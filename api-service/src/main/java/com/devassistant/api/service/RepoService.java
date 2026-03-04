package com.devassistant.api.service;

import com.devassistant.api.client.AIClient;
import com.devassistant.api.integration.GithubClient;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.stream.Collectors;

@Service
public class RepoService {
    private final GithubClient githubClient;
    private final ExecutorService githubExecutor;
    private final AIClient aiClient;

    public RepoService(
            GithubClient githubClient,
            AIClient aiClient,
            ExecutorService githubExecutor
    ) {
        this.githubClient = githubClient;
        this.githubExecutor = githubExecutor;
        this.aiClient = aiClient;
    }

    /*private List<String> getRelevantFiles(String issue, List<String>files) {
        Set<String> keywords = Arrays.stream(issue.toLowerCase().split("\\W+"))
                .filter(w -> w.length() > 2)
                .collect(Collectors.toSet());

        Map<String, Integer> scoreMap = new HashMap<>();

        for(String file:files) {
            String lowerFile = file.toLowerCase();
            // Step 2: filter only code files
            if (!(lowerFile.endsWith(".java") || lowerFile.endsWith(".js") ||
                    lowerFile.endsWith(".ts") || lowerFile.endsWith(".py") ||
                    lowerFile.endsWith(".jsx"))) {
                continue;
            }
            int score = 0;
            for(String keyword:keywords) {
                if(lowerFile.contains(keyword)){
                    score+=2;
                }
                if (lowerFile.contains("src") || lowerFile.contains("service") || lowerFile.contains("controller")) {
                    score += 1;
                }
                if (score > 0) {
                    scoreMap.put(file, score);
                }
            }

        }
        return scoreMap.entrySet().stream()
                .sorted((a,b) -> b.getValue()-a.getValue())
                .map(Map.Entry::getKey)
                .limit(5)
                .toList();
    }*/

    private List<Map<String, String>> getAllFileData(String owner, String repo) {
        List<Map<String, String>> tree = githubClient.getRepoTree(owner, repo);
        List<Map<String, String>> allFiles = new ArrayList<>();
        for(Map<String, String> node:tree) {
            if(node.get("type").equals("file")) {
                String path = node.get("path");
                // need to call this in a parallel way
                String content = githubClient.getFileContent(owner, repo, path);
                Map<String, String> fileData = new HashMap<>();
                fileData.put("path", path);
                fileData.put("content", content);
                allFiles.add(fileData);
            }
        }
        return allFiles;
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
            System.out.println("indexing repo...");
            List<Map<String, String>> allFiles = getAllFileData(owner, repo);
            aiClient.indexRepo(repoKey, sha, allFiles);
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
        /* List<Map<String, String>> tree = githubClient.getRepoTree(owner, repo);

        List<String> files = new ArrayList<>();
        for(Map<String, String> node:tree) {
            if(node.get("type").equals("file")) files.add(node.get("path"));
        }

        // later we will call ai-service for RAG based retrieval
        List<String> relevantFilePaths = getRelevantFiles(issueText, files);
        // System.out.println("relevant file paths size is: " + relevantFilePaths.size());

        List<CompletableFuture<String>> futures = relevantFilePaths.stream()
                .map(path -> CompletableFuture.supplyAsync(() -> {
                    try {
                        return githubClient.getFileContent(owner, repo, path);
                    } catch (Exception e) {
                        System.out.println("Exception for: " + path + " " + e);
                        return  "";
                        // throw new RuntimeException(e);
                    }
                }, githubExecutor))
                .toList();
        List<String> relevantFileContents = futures.stream()
                .map(f -> {
                    try {
                        return f.join();
                    } catch (Exception e) {
                        return "";
                    }
                })
                .toList();

        Map<String, Object> response = new HashMap<>();
        response.put("issue", issue);
        response.put("fileContents", relevantFileContents);

        return response;*/
    }

}
