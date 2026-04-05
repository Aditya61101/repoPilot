package com.devassistant.api.middleware;

import com.devassistant.api.dto.ErrorResponse;
import com.devassistant.api.exception.ErrorResponseWriter;
import com.devassistant.api.service.JWTService;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.jsonwebtoken.JwtException;
import jakarta.annotation.Nonnull;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
@RequiredArgsConstructor
public class JwtFilter extends OncePerRequestFilter {

    private final JWTService jwtService;
    private final ErrorResponseWriter errorResponseWriter;

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        String path = request.getServletPath();
        return path.startsWith("/api/auth");
    }

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            @Nonnull HttpServletResponse response,
            @Nonnull FilterChain filterChain
    ) throws ServletException, IOException {

        Cookie[] cookies = request.getCookies();
        String jwt = null;

        if(cookies!=null) {
            for(Cookie cookie: cookies) {
                if("auth_token".equals(cookie.getName())) {
                    jwt = cookie.getValue();
                    break;
                }
            }
        }

        if(jwt == null) {
            errorResponseWriter.write(response, HttpServletResponse.SC_UNAUTHORIZED, "Unauthorized", "No auth token provided");
            return;
        }

        try {
            Long userId = jwtService.parse(jwt);
            request.setAttribute("userId", userId);
            filterChain.doFilter(request, response);
        } catch (JwtException e) {
            System.out.println("Error in JwtFilter: " + e.getMessage());
            errorResponseWriter.write(response, HttpServletResponse.SC_UNAUTHORIZED, "Unauthorized", "Invalid auth token");
        }
    }
}
