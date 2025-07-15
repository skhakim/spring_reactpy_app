package com.example.springdemo;

import org.springframework.data.jpa.repository.JpaRepository;

public interface NameRepository extends JpaRepository<SpringDemoApplication.NameEntity, Integer> {
}
