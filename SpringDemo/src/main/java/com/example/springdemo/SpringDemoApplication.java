package com.example.springdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.Optional;
import java.util.concurrent.TimeUnit;

@SpringBootApplication
@RestController
@RequestMapping("/")
public class SpringDemoApplication {

    private final NameRepository repository;
    private final StringRedisTemplate redisTemplate;

    public SpringDemoApplication(NameRepository repository, StringRedisTemplate redisTemplate) {
        this.repository = repository;
        this.redisTemplate = redisTemplate;
    }

    public static void main(String[] args) {
        SpringApplication.run(SpringDemoApplication.class, args);
    }

    // DTO class for request
    public static class IdRequest {
        private Integer id;

        public IdRequest() {}

        public Integer getId() {
            return id;
        }

        public void setId(Integer id) {
            this.id = id;
        }
    }

    // DTO class for response
    public static class NameResponse {
        private String name;

        public NameResponse() {}

        public NameResponse(String name) {
            this.name = name;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }
    }

    @PostMapping(path = "getName", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public NameResponse getName(@RequestBody IdRequest request) {
        if (request == null || request.getId() == null) {
            return new NameResponse(null);
        }
        String cacheKey = "name:" + request.getId();

        // Try Redis cache first
        String cachedName = redisTemplate.opsForValue().get(cacheKey);
        if (cachedName != null) {
            System.out.println("Cache hit for id: " + request.getId());
            return new NameResponse(cachedName);
        } else {
            System.out.println("Cache miss for id: " + request.getId());
        }

        // Else fetch from DB
        Optional<NameEntity> entityOpt = repository.findById(request.getId());
        if (entityOpt.isPresent()) {
            String name = entityOpt.get().getName();
            // Cache in Redis with TTL 1 hour
            redisTemplate.opsForValue().set(cacheKey, name, 1, TimeUnit.HOURS);
            return new NameResponse(name);
        } else {
            // If not found, return null or empty name (customize as needed)
            return new NameResponse(null);
        }
    }

    // JPA Entity
    @Entity
    @Table(name = "name_entity")
    public static class NameEntity {
        @Id
        private Integer id;
        private String name;

        public NameEntity() {}

        public Integer getId() {
            return id;
        }

        public void setId(Integer id) {
            this.id = id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }
    }
}
