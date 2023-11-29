package com.example.gradeaverage;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.*;

@Controller
@RequestMapping
public class AverageCalculationController {

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public ResponseEntity<String> index(@RequestParam("mark_1") String mark_1, @RequestParam("mark_2") String mark_2, @RequestParam("mark_3") String mark_3, @RequestParam("mark_4") String mark_4, @RequestParam("mark_5") String mark_5) throws JsonProcessingException {
        // Create HashMap for response
        Map<String, String> mp = new HashMap<>();
        try {
            // Validate the data
            ArrayList<String> paramsToBeValidated = new ArrayList<>();
            paramsToBeValidated.add(mark_1);
            paramsToBeValidated.add(mark_2);
            paramsToBeValidated.add(mark_3);
            paramsToBeValidated.add(mark_4);
            paramsToBeValidated.add(mark_5);
            ArrayList<Integer> paramsThatAreInts = new ArrayList();
            for (String item : paramsToBeValidated) {
                if (!item.isEmpty()) {
                    try {
                        paramsThatAreInts.add(Integer.parseInt(item));
                    } catch (NumberFormatException nfe) {
                        System.out.println(item + " is not an Integer");
                        throw new NumberFormatException();
                    }
                }
            }
            // Calculate Average Grade
            float average = 0;
            for (Integer item : paramsThatAreInts) {
                average += item;
            }
            average = average / paramsThatAreInts.size();
            // Add to hashmap
            mp.put("average_mark", Float.toString(average));
        }catch (NumberFormatException nfe) {
            mp.put("error_msg", "All marks need to be integers");
        }
        catch (Exception ex){
            // Add the error message to the response
            mp.put("error_msg", "There was an unexpected error during the calculation of the average mark");
        }
        // Convert HashMap to JSON
        ObjectMapper mapper = new ObjectMapper();
        String jsonResponse = mapper.writeValueAsString(mp);

        // Set Headers
        HttpHeaders responseHeaders = new HttpHeaders();
        responseHeaders.set("Content-type", "application/json");
        responseHeaders.set("Access-Control-Allow-Origin", "*");
        // Return our Response
        return ResponseEntity.ok()
                .headers(responseHeaders)
                .body(jsonResponse);
    }

    @RequestMapping(value = "/Home", method = RequestMethod.GET)
    public ResponseEntity<String> home(){
        return ResponseEntity.ok().body("Hello");
    }
}
