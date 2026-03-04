package com.devassistant.api.integration;

import com.devassistant.api.exception.GithubException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@Service
public class GithubClient {
    @Value("${github.token}")
    private String token;

    @Value("${github.base-url}")
    private String baseUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    private List<Map<String, String>> extractRepoTree(Map<String,Object> treeResponse) {
        List<Map<String, String>> result = new ArrayList<>();
        List<Map<String,Object>> tree = (List<Map<String,Object>>) treeResponse.get("tree");
        for(Map<String, Object>node : tree) {
            String type = (String) node.get("type");
            /* skipping unwanted types */
            if(!type.equals("blob") && !type.equals("tree")) continue;

            Map<String, String> item = new HashMap<>();
            item.put("path", (String) node.get("path"));
            item.put("type", type.equals("blob") ? "file" : "dir");
            result.add(item);
        }
        return result;
    }

    private Object makeGetRequest(String url) {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer "+ token);
        /* tells what kind of response the API would accept */
        headers.set("Accept", "application/vnd.github+json");

        HttpEntity<String> entity = new HttpEntity<>(headers);
        try {
            ResponseEntity<Object> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    entity,
                    Object.class
            );
            return response.getBody();
        } catch (HttpClientErrorException e) {
            throw new GithubException(e.getStatusCode(), e.getResponseBodyAsString());
        }
    }

    public Object getRepos(String owner) {
        String url = baseUrl + "/users/" + owner + "/repos";
        return makeGetRequest(url);
    }

    public Object getIssues(String owner, String repo) {
        String url = baseUrl + "/repos/" + owner + "/" + repo + "/issues";
        return makeGetRequest(url);
    }

    public Object getFiles(String owner, String repo) {
        String url = baseUrl + "/repos/" + owner + "/" + repo + "/contents";
        return makeGetRequest(url);
    }

    public List<Map<String, String>> getRepoTree(String owner, String repo) {
        /* getting repo details */
        String repoUrl = baseUrl + "/repos/" + owner + "/" + repo;
        Map<String, Object> repoDetails = (Map<String, Object>) makeGetRequest(repoUrl);
        String branch = (String) repoDetails.get("default_branch");
        /* get full tree */
        String treeUrl = baseUrl + "/repos/" + owner + "/" + repo + "/git/trees/" + branch + "?recursive=1";
        Map<String, Object> treeResponse = (Map<String,Object>) makeGetRequest(treeUrl);
        return extractRepoTree(treeResponse);
    }

    public List<Map<String, String>> getRepoTreeBySHA(String owner, String repo, String sha) {
        String treeUrl = baseUrl + "/repos/" + owner + "/" + repo + "/git/trees/" + sha + "?recursive=1";
        Map<String, Object> treeResponse = (Map<String,Object>) makeGetRequest(treeUrl);
        return extractRepoTree(treeResponse);
    }

    public String getFileContent(String owner, String repo, String path) {
        String url = baseUrl + "/repos/" + owner + "/" + repo + "/contents/" + path;
        Map<String, Object> response = (Map<String, Object>) makeGetRequest(url);

        String encoded = (String) response.get("content");

        // remove newlines
        encoded = encoded.replace("\n", "");
        byte[] decodeBytes = Base64.getDecoder().decode(encoded);

        return new String(decodeBytes);
    }

    public Object getIssue(String owner, String repo, int issueNumber) {
        String url = baseUrl + "/repos/" + owner + "/" + repo + "/issues/" + issueNumber;
        return makeGetRequest(url);
    }

    public String getLatestCommitSha(String owner, String repo) {
        String url = baseUrl + "/repos/" + owner + "/" + repo + "/commits";
        List<Map<String, Object>> commits = (List<Map<String, Object>>) makeGetRequest(url);
        if(commits.isEmpty()) return "";
        // commits are in descending order
        Map<String, Object> latestCommit = commits.getFirst();
        String latestSha = (String) latestCommit.get("sha");
        System.out.println("latest commit of given repo: " + latestSha);
        return latestSha;
    }
}
