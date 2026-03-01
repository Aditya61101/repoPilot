package com.devassistant.api.controller;

import com.devassistant.api.service.RepoService;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class RepoController {
    private final RepoService repoService;

    public RepoController(RepoService repoService) {
        this.repoService = repoService;
    }

    @GetMapping("/repos")
    public Object getRepos(@RequestParam String owner) {
        return repoService.getRepos(owner);
    }

    @GetMapping("/issues")
    public Object getIssues(@RequestParam String owner, @RequestParam String repo) {
        return repoService.getIssues(owner, repo);
    }

    @GetMapping("/files")
    public Object getFiles(@RequestParam String owner, @RequestParam String repo) {
        return repoService.getFiles(owner, repo);
    }

    @GetMapping("/repo-tree")
    public List<Map<String, String>> getRepoTree(@RequestParam String owner, @RequestParam String repo) {
        return repoService.getRepoTree(owner, repo);
    }

    @GetMapping("/file-content")
    public String getFileContent(@RequestParam String owner, @RequestParam String repo, @RequestParam String path) {
        return repoService.getFileContent(owner, repo, path);
    }
}
