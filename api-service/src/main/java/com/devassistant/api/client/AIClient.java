package com.devassistant.api.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.List;
import java.util.Map;

@Service
public class AIClient {
    private final WebClient webClient;

    public AIClient(WebClient.Builder builder, @Value("${ai-service.base-url}") String aiBaseURL) {
        System.out.println("ai-service base url is: "+ aiBaseURL);
        webClient = builder.baseUrl(aiBaseURL).build();
    }

    public boolean ensureIndexed(String repoKey, String sha) {
        Map<String, String> body = Map.of("repo_key", repoKey, "commit_sha", sha);

        Map response = webClient.post()
                .uri("/ensure-indexed")
                .bodyValue(body)
                .retrieve()
                .bodyToMono(Map.class)
                .block();

        return (Boolean) response.get("needs_index");
    }

    public void indexRepo(String repoKey, String sha, List<Map<String, String>> files) {
        Map<String, Object> body = Map.of(
                "repo_key", repoKey,
                "commit_sha", sha,
                "files", files
        );

        webClient.post()
                .uri("/index")
                .bodyValue(body)
                .retrieve()
                .bodyToMono(Void.class)
                .block();
    }

    public String analyze(String repoKey, String issue) {
        Map<String, String> body = Map.of(
                "repo_key", repoKey,
                "issue", issue
        );

        Map response = webClient.post()
                .uri("/analyze")
                .bodyValue(body)
                .retrieve()
                .bodyToMono(Map.class)
                .block();

        return (String) response.get("analysis");
    }
}
