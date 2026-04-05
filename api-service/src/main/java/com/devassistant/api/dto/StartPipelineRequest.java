package com.devassistant.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class StartPipelineRequest {
    @JsonProperty("repo_key")
    private String repoKey;

    private String issue;

    @JsonProperty("commit_sha")
    private String commitSha;

}
