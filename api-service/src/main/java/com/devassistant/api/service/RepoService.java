package com.devassistant.api.service;

import com.devassistant.api.integration.GithubClient;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class RepoService {
    private final GithubClient githubClient;

    public RepoService(GithubClient githubClient) {
        this.githubClient = githubClient;
    }

    public Object getRepos(String owner) {
        return githubClient.getRepos(owner);
    }

    public Object getIssues(String owner, String repo) { return githubClient.getIssues(owner, repo); }

    public Object getFiles(String owner, String repo) { return githubClient.getFiles(owner, repo); }

    public List<Map<String, String>> getRepoTree(String owner, String repo) { return githubClient.getRepoTree(owner, repo); }

    public String getFileContent(String owner, String repo, String path) { return githubClient.getFileContent(owner, repo, path); }
}
