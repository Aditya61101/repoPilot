package com.devassistant.api.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class AuthService {
    @Value("${github.redirect-url}")
    private String redirectUri;

    @Value("${github.client-id}")
    private String clientID;

    @Value("${github.client-secret}")
    private String clientSecret;

    private final Set<String> stateStore = ConcurrentHashMap.newKeySet();
    private final WebClient webClient;

    // SpringBoot won't automatically inject WebClient, we either need a @Config or use builder.build
    public AuthService(WebClient.Builder builder) {
        this.webClient = builder.build();
    }

    private String exchangeCodeForToken(String code) {
        System.out.println("CLIENT ID: "+ clientID);
        System.out.println("CLIENT SECRET: "+clientSecret);

        Map response = webClient.post()
                .uri("https://github.com/login/oauth/access_token")
                .header("Accept", "application/json")
                .bodyValue(Map.of(
                        "client_id", clientID,
                        "client_secret", clientSecret,
                        "code", code,
                        "redirect_uri", redirectUri
                ))
                .retrieve()
                .bodyToMono(Map.class)
                .block();

        System.out.println("FULL RESPONSE: " + response);
        return (String) response.get("access_token");
    }

    private Map<String,Object> fetchGithubUser(String token) {
        return webClient.get()
                .uri("https://api.github.com/user")
                .header("Authorization", "Bearer "+token)
                .retrieve()
                .bodyToMono(Map.class)
                .block();
    }

    public String buildRedirectURL() {
        // for CSRF protection
        String state = UUID.randomUUID().toString();
        stateStore.add(state);

        return UriComponentsBuilder
                .fromUriString(
          "https://github.com/login/oauth/authorize")
                .queryParam("client_id", clientID)
                .queryParam("redirect_uri", redirectUri)
                .queryParam("scope", "repo")
                .queryParam("state", state)
                .build()
                .toUriString();
    }

    public Map<String, Object> handleCallback(String code, String state) {
        // removing after validation
        if(!stateStore.remove(state)) {
            throw new RuntimeException("Invalid state");
        }

        String accessToken = exchangeCodeForToken(code);
        Map<String, Object> user = fetchGithubUser(accessToken);

        return Map.of(
                "token", accessToken,
                "user", user
        );
    }
}
