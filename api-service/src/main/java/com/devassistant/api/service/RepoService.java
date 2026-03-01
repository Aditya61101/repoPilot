package com.devassistant.api.service;

import com.devassistant.api.integration.GithubClient;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class RepoService {
    private final GithubClient githubClient;

    public RepoService(GithubClient githubClient) {
        this.githubClient = githubClient;
    }

    private List<String> getRelevantFiles(String issue, List<String>files) {
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
        Map<String, Object> issue = (Map<String, Object>) githubClient.getIssue(owner, repo, issueNumber);
//        System.out.println("issue detail for" + issueNumber + "is: " + issue.get("title"));

        String title = (String) issue.get("title");
        String body = (String) issue.get("body");

        String issueText = (title != null ? title : "") + " " + (body != null ? body : "");

        List<Map<String, String>> tree = githubClient.getRepoTree(owner, repo);

        List<String> files = new ArrayList<>();
        for(Map<String, String> node:tree) {
            if(node.get("type").equals("file")) files.add(node.get("path"));
        }

        // later we will call ai-service for RAG based retrieval
        List<String> relevantFilePaths = getRelevantFiles(issueText, files);
        // System.out.println("relevant file paths size is: " + relevantFilePaths.size());
        List<String> relevantFileContents = new ArrayList<>();
        // later we may do parallel api calls
        for(String path:relevantFilePaths) {
        // System.out.println("path is: "+ path);
            String content = githubClient.getFileContent(owner, repo, path);
            relevantFileContents.add(content);
        }

        Map<String, Object> response = new HashMap<>();
        response.put("issue", issue);
        response.put("fileContents", relevantFileContents);

        return response;
    }

}
