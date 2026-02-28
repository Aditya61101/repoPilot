package com.devassistant.api.service;

import com.devassistant.api.integration.GithubClient;
import org.springframework.stereotype.Service;

@Service
public class RepoService {
    private final GithubClient githubClient;

    public RepoService(GithubClient githubClient) {
        this.githubClient = githubClient;
    }

    public String getRepos(String owner) {
        return githubClient.getRepos(owner);
    }
}
