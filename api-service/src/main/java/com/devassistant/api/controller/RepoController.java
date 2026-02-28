package com.devassistant.api.controller;

import com.devassistant.api.service.RepoService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class RepoController {
    private final RepoService repoService;

    public RepoController(RepoService repoService) {
        this.repoService = repoService;
    }

    @GetMapping("/repos")
    public String getRepos(@RequestParam String owner) {
        return repoService.getRepos(owner);
    }
}
