package com.devassistant.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;

public class GithubException extends RuntimeException {
    private final HttpStatusCode statusCode;

    public GithubException(HttpStatusCode statusCode, String message) {
        super(message);
        this.statusCode = statusCode;
    }
    public HttpStatusCode getStatusCode() {
        return this.statusCode;
    }
}
