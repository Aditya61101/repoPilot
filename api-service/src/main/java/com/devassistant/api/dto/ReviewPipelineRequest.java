package com.devassistant.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

import java.util.Map;

@Getter
@Setter
public class ReviewPipelineRequest {
    @JsonProperty("thread_id")
    private String threadId;

    @JsonProperty("file_reviews")
    private Map<String, Object> fileReviews;
}
