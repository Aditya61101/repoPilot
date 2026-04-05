package com.devassistant.api.service;

import com.devassistant.api.dto.UserResponse;
import com.devassistant.api.entity.User;
import com.devassistant.api.repository.UserRepository;

import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseCookie;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriComponentsBuilder;

import java.time.Duration;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
@RequiredArgsConstructor
public class AuthService {
    @Value("${github.redirect-url}")
    private String redirectUri;

    @Value("${github.client-id}")
    private String clientID;

    @Value("${github.client-secret}")
    private String clientSecret;

    private final Set<String> stateStore = ConcurrentHashMap.newKeySet();
    private WebClient webClient;

    private final WebClient.Builder webClientBuilder;
    private final JWTService jwtService;
    private final UserRepository userRepository;

    @PostConstruct
    public void init() {
        this.webClient = webClientBuilder.build();
    }

    private String exchangeCodeForToken(String code) {
        // System.out.println("CLIENT ID: "+ clientID);
        // System.out.println("CLIENT SECRET: "+clientSecret);

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
        if(response==null || response.get("access_token")==null) {
            throw new RuntimeException("Token exchange failed: ");
        }
        return (String) response.get("access_token");
    }

    private User saveOrUpdateUser(Map<String, Object> user, String token) {
        String githubId = String.valueOf(user.get("id"));
        String username = (String) user.get("login");
        Optional<User> existing = userRepository.findByGithubId(githubId);

        if(existing.isPresent()) {
            User existingUser = existing.get();
            // updating the github_token with the new token came in exchange with the code.
            existingUser.setAccessToken(token);
            return userRepository.save(existingUser);
        }
        User newUser = new User();
        newUser.setUsername(username);
        newUser.setAccessToken(token);
        newUser.setGithubId(githubId);
        return userRepository.save(newUser);
    }

    private Map fetchGithubUser(String token) {
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

    public String handleCallback(String code, String state) {
        // removing after validation
        if(!stateStore.remove(state)) {
            throw new RuntimeException("Invalid state");
        }

        String accessToken = exchangeCodeForToken(code);
        Map<String, Object> githubUser = fetchGithubUser(accessToken);
        User user = saveOrUpdateUser(githubUser, accessToken);

        // generate jwt and return
        return jwtService.generate(user.getId());
    }

    public UserResponse handleMe(String token) {
        Long userId = jwtService.parse(token);
        User user = userRepository.findById(userId).orElseThrow();
        return new UserResponse(
                user.getId(),
                user.getUsername(),
                user.getGithubId()
        );
    }

    public String getGithubToken(Long userId) {
        User user = userRepository.findById(userId).orElseThrow(() -> new RuntimeException("User not found"));
        return user.getAccessToken();
    }
}
