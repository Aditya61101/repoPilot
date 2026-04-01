package com.devassistant.api.controller;

import com.devassistant.api.service.AuthService;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
@RequestMapping("/auth")
public class AuthController {
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @GetMapping("/github")
    public void redirect(HttpServletResponse response) throws IOException {
        String url = this.authService.buildRedirectURL();
        response.sendRedirect(url);
    }

    @GetMapping("/github/callback")
    public ResponseEntity<?> callback(@RequestParam String code, @RequestParam String state) {
        return ResponseEntity.ok(authService.handleCallback(code, state));
    }

}
