package com.devassistant.api.controller;

import com.devassistant.api.client.AIClient;
import com.devassistant.api.dto.ReviewPipelineRequest;
import com.devassistant.api.dto.StartPipelineRequest;
import com.devassistant.api.service.RepoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.StreamingResponseBody;

import java.util.Map;

@RestController
@RequestMapping("/api/pipeline")
@RequiredArgsConstructor
public class PipelineController {
    private final AIClient aiClient;

    @PostMapping("/start")
    public Map<String, String> startPipeline(@RequestBody StartPipelineRequest req) {
        return aiClient.startPipeline(req);
    }

    @GetMapping("/stream")
    public ResponseEntity<StreamingResponseBody> streamPipeline(@RequestParam String threadId) {
        StreamingResponseBody stream = aiClient.stream(threadId);
        return ResponseEntity.ok()
                .header("Content-Type", "text/event-stream")
                .body(stream);
    }

    @PostMapping("/review")
    public Map<String, String> reviewPipeline(@RequestBody ReviewPipelineRequest req) {
        return aiClient.review(req);
    }
}
