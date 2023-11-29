package com.example.gradereview

import com.fasterxml.jackson.core.JsonProcessingException
import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.http.HttpHeaders
import org.springframework.http.ResponseEntity
import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestMethod
import org.springframework.web.bind.annotation.RequestParam

@Controller
@RequestMapping
class GradeReview {

    @RequestMapping(value = ["/"], method = [RequestMethod.GET])
    @Throws(JsonProcessingException::class)
    fun index(
        @RequestParam("mark_1") mark_1: String,
        @RequestParam("mark_2") mark_2: String,
        @RequestParam("mark_3") mark_3: String,
        @RequestParam("mark_4") mark_4: String,
        @RequestParam("mark_5") mark_5: String
    ): ResponseEntity<String?> {
        println("Processing Request")
        // Create HashMap for response
        val mp: MutableMap<String, String> = HashMap()
        try {
            // Add grades to HashMap
            mp["grade_1"] = determineNextGrade(mark_1.toDouble()).toString()
            mp["grade_2"] = determineNextGrade(mark_2.toDouble()).toString()
            mp["grade_3"] = determineNextGrade(mark_3.toDouble()).toString()
            mp["grade_4"] = determineNextGrade(mark_4.toDouble()).toString()
            mp["grade_5"] = determineNextGrade(mark_5.toDouble()).toString()

        }catch (ex: NumberFormatException){
            // Add error_msg to HashMap
            mp.clear()
            mp["error_msg"] = "All marks need to be numbers"
        }catch (ex: Exception){
            // Add error_msg to HashMap
            mp["error_msg"] = "Could not determine the next grade"
        }

        // Convert HashMap to JSON
        val mapper = ObjectMapper()
        val jsonResponse = mapper.writeValueAsString(mp)

        // Set Headers
        val responseHeaders = HttpHeaders()
        responseHeaders.set("Content-type", "application/json")
        responseHeaders.set("Access-Control-Allow-Origin", "*")

        // Return our Response
        return ResponseEntity.ok()
            .headers(responseHeaders)
            .body<String>(jsonResponse)
    }

    private fun determineNextGrade(mark: Double): Double {
        return if (mark >= 80) {
            0.0
        } else if (mark >= 70) {
            80 - mark
        } else if (mark >= 60) {
            70 - mark
        } else if (mark >= 50) {
            60 - mark
        } else if (mark >= 40) {
            50 - mark
        } else {
            40 - mark
        }
    }
}