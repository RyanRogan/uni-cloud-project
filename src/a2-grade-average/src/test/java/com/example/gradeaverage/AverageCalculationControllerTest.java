package com.example.gradeaverage;

import org.json.JSONException;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.web.client.TestRestTemplate;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
public class AverageCalculationControllerTest {
    private static final String MARK_1_ERR = "Hi";
    private static final String MARK_1 = "5";
    private static final String MARK_2 = "5";
    private static final String MARK_3 = "5";
    private static final String MARK_4 = "5";
    private static final String MARK_5 =  "5";
    private static final String GET_REQUEST = "?module_1=q&mark_1="+MARK_1+"&module_2=q&mark_2="+MARK_2+"&module_3=q&mark_3="+MARK_3+"&module_4=q&mark_4="+MARK_4+"&module_5=q&mark_5="+MARK_5;
    private static final String GET_REQUEST_ERROR = "?module_1=q&mark_1="+MARK_1_ERR+"&module_2=q&mark_2="+MARK_2+"&module_3=q&mark_3="+MARK_3+"&module_4=q&mark_4="+MARK_4+"&module_5=q&mark_5="+MARK_5;

    @Value("${local.server.port}")
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    public void rootShouldReturnAverage() throws Exception {
        System.out.println("The Port is " + port);
        assertThat(this.restTemplate.getForObject("http://localhost:" + port + "/" + GET_REQUEST,
                    String.class)).contains("5");
    }
    @Test
    public void ShouldReturnErrorMsgWhenMarkIsNotInteger() throws JSONException {
        JSONObject res_json = new JSONObject(this.restTemplate.getForObject("http://localhost:" + port + "/" + GET_REQUEST_ERROR, String.class));
        assertThat(res_json.get("error_msg")).isEqualTo("All marks need to be integers");
    }
}
