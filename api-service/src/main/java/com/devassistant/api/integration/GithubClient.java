package com.devassistant.api.integration;

import com.devassistant.api.exception.GithubException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

@Service
public class GithubClient {
    @Value("${github.token}")
    private String token;

    private final RestTemplate restTemplate = new RestTemplate();

    public String getRepos(String owner) {
        String url = "https://api.github.com/users/" + owner + "/repos";

        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer "+token);
        headers.set("Accept", "application/vnd.github+json");

        HttpEntity<String> entity = new HttpEntity<>(headers);
        try {
            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    entity,
                    String.class
            );
            return response.getBody();
        } catch (HttpClientErrorException e) {
                throw new GithubException(e.getStatusCode(), e.getResponseBodyAsString());
        }
    }
}
