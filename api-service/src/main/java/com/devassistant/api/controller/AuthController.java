package com.devassistant.api.controller;

import com.devassistant.api.dto.UserResponse;
import com.devassistant.api.entity.User;
import com.devassistant.api.service.AuthService;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.time.Duration;
import java.util.Objects;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {
    @Value("${frontend.base-url}")
    private String frontend;

    @Value("${spring.application.env}")
    private String env;

    private final AuthService authService;

    @GetMapping("/github")
    public void redirect(HttpServletResponse response) throws IOException {
        String url = this.authService.buildRedirectURL();
        response.sendRedirect(url);
    }

    @GetMapping("/github/callback")
    public void callback(@RequestParam String code, @RequestParam String state, HttpServletResponse response) throws IOException {
        String jwt = authService.handleCallback(code, state);
        boolean secure = env.equals("prod");
        ResponseCookie cookie = ResponseCookie.from("auth_token", jwt)
                .httpOnly(true)
                .secure(secure)
                .path("/")
                .maxAge(Duration.ofDays(1))
                .sameSite("Lax")
                .build();

        response.addHeader(HttpHeaders.SET_COOKIE, cookie.toString());
        response.sendRedirect(frontend);
    }

    @GetMapping("/me")
    public ResponseEntity<UserResponse> me(@CookieValue(value = "auth_token", required = false) String token) {
        if (token == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        return ResponseEntity.ok(authService.handleMe(token));
    }

}
