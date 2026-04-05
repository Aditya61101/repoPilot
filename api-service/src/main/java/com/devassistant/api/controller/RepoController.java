package com.devassistant.api.controller;

import com.devassistant.api.service.RepoService;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/repos")
public class RepoController {
    private final RepoService repoService;

    public RepoController(RepoService repoService) {
        this.repoService = repoService;
    }

    @GetMapping("/")
    public List<Map<String,String>> getRepos(@RequestAttribute("userId") Long userId) {
        return repoService.getRepos(userId);
    }

    @GetMapping("/issues")
    public Map<String,Object> getIssues(@RequestAttribute("userId") Long userId, @RequestParam String owner, @RequestParam String repo) {
        return repoService.getIssues(owner, repo, userId);
    }

    @GetMapping("/v2/files")
    public Object getFilesV2(@RequestAttribute("userId") Long userId , @RequestParam String owner, @RequestParam String repo, @RequestParam String commitSha) {
        return repoService.getAllFileData(owner, repo, commitSha, userId);
    }

    @GetMapping("/files")
    public Object getFiles(@RequestAttribute("userId") Long userId, @RequestParam String owner, @RequestParam String repo) {
        return repoService.getFiles(owner, repo, userId);
    }

    @GetMapping("/repo-tree")
    public List<Map<String, String>> getRepoTree(@RequestAttribute("userId") Long userId, @RequestParam String owner, @RequestParam String repo) {
        return repoService.getRepoTree(owner, repo, userId);
    }

    @GetMapping("/file-content")
    public String getFileContent(@RequestAttribute("userId") Long userId, @RequestParam String owner, @RequestParam String repo, @RequestParam String path) {
        return repoService.getFileContent(owner, repo, path, userId);
    }

}
