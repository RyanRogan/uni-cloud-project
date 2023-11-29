package com.example.gradereview

import org.assertj.core.api.Assertions
import org.json.JSONObject
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment
import org.springframework.boot.test.web.client.TestRestTemplate


@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class GradeReviewTest {
    @Value("\${local.server.port}")
    private val port = 0

    @Autowired
    private val restTemplate: TestRestTemplate? = null
    @Test
    @Throws(Exception::class)
    fun rootShouldReturnNextGradeBoundariesForEachGrade() {
        println("The Port is $port")
        val resp = restTemplate!!.getForObject(
            "http://localhost:$port/$GET_REQUEST",
            String::class.java
        )
        println("Response: $resp")
        val reply = JSONObject(resp)
        val nextGrade = "35.0"
        Assertions.assertThat(reply.get("grade_1")).isEqualTo(nextGrade)
        Assertions.assertThat(reply.get("grade_2")).isEqualTo(nextGrade)
        Assertions.assertThat(reply.get("grade_3")).isEqualTo(nextGrade)
        Assertions.assertThat(reply.get("grade_4")).isEqualTo(nextGrade)
        Assertions.assertThat(reply.get("grade_5")).isEqualTo(nextGrade)
    }

    @Test
    @Throws(Exception::class)
    fun rootShouldReturnErrorWhenDataIsMissing() {
        println("The Port is $port")
        val resp = restTemplate!!.getForObject(
            "http://localhost:$port/",
            String::class.java
        )
        println("Response: $resp")
        val reply = JSONObject(resp)
        val errorMsg = "Bad Request"
        Assertions.assertThat(reply.get("error")).isEqualTo(errorMsg)
    }

    @Test
    @Throws(Exception::class)
    fun rootShouldReturnErrorWhenDataIsNotNumeric() {
        println("The Port is $port")
        val resp = restTemplate!!.getForObject(
            "http://localhost:$port/$GET_REQUEST_Err",
            String::class.java
        )
        println("Response: $resp")
        val reply = JSONObject(resp)
        val errorMsg = "All marks need to be numbers"
        Assertions.assertThat(reply.get("error_msg")).isEqualTo(errorMsg)
    }

    companion object {
        private const val MARK_1 = "5"
        private const val MARK_2 = "5"
        private const val MARK_3 = "5"
        private const val MARK_3_Err = "hello_world"
        private const val MARK_4 = "5"
        private const val MARK_5 = "5"
        private const val GET_REQUEST =
            "?module_1=q&mark_1=$MARK_1&module_2=q&mark_2=$MARK_2&module_3=q&mark_3=$MARK_3&module_4=q&mark_4=$MARK_4&module_5=q&mark_5=$MARK_5"
        private const val GET_REQUEST_Err =
            "?module_1=q&mark_1=$MARK_1&module_2=q&mark_2=$MARK_2&module_3=q&mark_3=$MARK_3_Err&module_4=q&mark_4=$MARK_4&module_5=q&mark_5=$MARK_5"
    }
}
