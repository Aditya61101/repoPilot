package com.devassistant.api.service;

import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;

import com.devassistant.api.client.AIClient;
import com.devassistant.api.integration.GithubClient;

@Service
public class RepoService {
    private final GithubClient githubClient;
    private final ExecutorService githubExecutor;
    private final AIClient aiClient;

    private static final Set<String> BLOCKED_EXTENSIONS = Set.of(
            ".png",".jpg",".jpeg",".gif",".webp",".ico",".svg",
            ".mp4", ".mp3", ".wav",
            ".zip",".tar",".gz",".rar",".7z",
            ".class",".jar",".war",".o",".so",".dll",".exe",".dylib",
            ".map", ".min.js", ".min.css"
    );
    private static final List<String> BLOCKED_DIRS = List.of(
            "/node_modules/", "/dist/",  "/build/", "/coverage/", "/target/",  "/bin/",
            "/obj/", "/.git/",  "/venv/", "/.venv/",  "/__pycache__/");

    public RepoService(
            GithubClient githubClient,
            AIClient aiClient,
            ExecutorService githubExecutor
    ) {
        this.githubClient = githubClient;
        this.githubExecutor = githubExecutor;
        this.aiClient = aiClient;
    }

    private boolean shouldIndex(String path) {
        String lower = path.toLowerCase();
        for(String dir:BLOCKED_DIRS) {
            if(lower.contains(dir)) return false;
        }
        int dot = lower.lastIndexOf(".");
        if(dot!=-1) {
            String ext = lower.substring(dot);
            return !BLOCKED_EXTENSIONS.contains(ext);
        }
        if(lower.endsWith("package-lock.json") || lower.endsWith("yarn.lock") || lower.endsWith("pnpm-lock.yaml")) {
            return false;
        }
        return true;
    }

    private List<Map<String, String>> getAllFileData(String owner, String repo, String sha) {
        List<Map<String, String>> tree = githubClient.getRepoTreeBySHA(owner, repo, sha);

        List<String> paths = tree.stream()
                .filter(n -> "file".equals(n.get("type")))
                .map(n -> n.get("path"))
                .filter(this::shouldIndex)
                .toList();

        List<CompletableFuture<Map<String, String>>> futures = paths.stream()
                .map(path -> CompletableFuture.supplyAsync(() -> {
                    try {
                        String content = githubClient.getFileContent(owner, repo, path);
                        Map<String, String> fileData = new HashMap<>();
                        fileData.put("path", path);
                        fileData.put("content", content);
                        return fileData;
                    } catch (Exception e) {
                        System.out.println("failed to fetch: "+ path);
                        System.out.println("exception occurred: "+ e.getMessage());
                        return null;
                    }
                }, githubExecutor))
                .toList();
        return futures.stream()
                .map(CompletableFuture::join)
                .filter(Objects::nonNull)
                .toList();
    }

    public Object getRepos(String owner) {
        return githubClient.getRepos(owner);
    }

    public Object getIssues(String owner, String repo) { return githubClient.getIssues(owner, repo); }

    public Object getFiles(String owner, String repo) { return githubClient.getFiles(owner, repo); }

    public List<Map<String, String>> getRepoTree(String owner, String repo) { return githubClient.getRepoTree(owner, repo); }

    public String getFileContent(String owner, String repo, String path) { return githubClient.getFileContent(owner, repo, path); }

    public Map<String, Object> analyzeIssue(String owner, String repo, int issueNumber) {
        System.out.println("inside analyze issues service");
        String repoKey = owner + "/" + repo;
        // Step 1: get commit SHA for given Repo
        String sha = githubClient.getLatestCommitSha(owner, repo);
        if(sha.isEmpty()) return Map.of(
                "error", "No commits found"
        );
        // step 2: send ai-service repoKey(owner, repo), commit SHA to check whether embedding exists or not
        boolean needsIndex = aiClient.ensureIndexed(repoKey, sha);
        // step 3: if it doesn't exist(need_indexing=True) then we fetch file paths and content and send it to ai-service for indexing
        if(needsIndex) {
            System.out.println("extracting all files content...");
            List<Map<String, String>> allFiles = getAllFileData(owner, repo, sha);
            System.out.println("all files content extracted...");
            Map<String,Object> response = (Map<String,Object>) aiClient.indexRepo(repoKey, sha, allFiles);
            System.out.println("response from indexing repo: "+ response.get("message"));
            if(!(Boolean)(response.get("status"))) return Map.of(
                    "error", "Internal Server Error"
            );
        }
        // step 4: after indexing, we again call ai-service for analysis
        Map<String, Object> issue = (Map<String, Object>) githubClient.getIssue(owner, repo, issueNumber);
        System.out.println("issue detail for " + issueNumber + " is: " + issue.get("title"));

        String title = (String) issue.get("title");
        String body = (String) issue.get("body");
        String issueText = (title != null ? title : "") + " " + (body != null ? body : "");

        String analysis = aiClient.analyze(repoKey, issueText);
        return Map.of(
                "issue", issue,
                "analysis", analysis
        );
    }

}
