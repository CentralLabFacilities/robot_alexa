/**
 * Author: flier@techfak.uni-bielefeld.de
 * <p>
 * Copyright 2014-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * <p>
 * Licensed under the Apache License, Version 2.0 (the "License"). You may not use
 * this file except in compliance with the License. A copy of the License is located at
 * <p>
 * http://aws.amazon.com/apache2.0/
 * <p>
 * or in the "license" file accompanying this file. This file is distributed on an "AS IS"
 * BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 * for the specific language governing permissions and limitations under the License.
 */

package pepperemote;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.amazon.speech.slu.Intent;
import com.amazon.speech.speechlet.IntentRequest;
import com.amazon.speech.speechlet.LaunchRequest;
import com.amazon.speech.speechlet.Session;
import com.amazon.speech.speechlet.SessionEndedRequest;
import com.amazon.speech.speechlet.SessionStartedRequest;
import com.amazon.speech.speechlet.Speechlet;
import com.amazon.speech.speechlet.SpeechletException;
import com.amazon.speech.speechlet.SpeechletResponse;
import com.amazon.speech.ui.PlainTextOutputSpeech;
import com.amazon.speech.ui.Reprompt;
import com.amazon.speech.ui.SimpleCard;
import com.amazonaws.util.json.JSONArray;
import com.amazonaws.util.json.JSONException;
import com.amazonaws.util.json.JSONObject;
import com.amazonaws.util.json.JSONTokener;
import robotremote.HttpClientGet;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.nio.charset.Charset;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;

import org.apache.commons.io.IOUtils;

/**
 * This class implements an Alexa Skill that finds available meals based on the
 * desired day and kind of food (vital, vegetarian, meal of the day ...)
 */
public class PepperSpeechlet implements Speechlet {

    private static final Logger log = LoggerFactory.getLogger(PepperSpeechlet.class);
    HttpClientGet httpClientGet = new HttpClientGet();

    @Override
    public void onSessionStarted(final SessionStartedRequest request, final Session session) throws SpeechletException {
        log.info("onSessionStarted requestId={}, sessionId={}", request.getRequestId(), session.getSessionId());
    }

    @Override
    public SpeechletResponse onLaunch(final LaunchRequest request, final Session session) throws SpeechletException {
        log.info("onLaunch requestId={}, sessionId={}", request.getRequestId(), session.getSessionId());
        return getNewWelcomeResponse();
    }

    @Override
    public SpeechletResponse onIntent(final IntentRequest request, final Session session) throws SpeechletException {
        log.info("onIntent requestId={}, sessionId={}", request.getRequestId(), session.getSessionId());

        Intent intent = request.getIntent();
        String intentName = (intent != null) ? intent.getName() : null;
        String cmd = "";
        String action = "";

        if ("GetNewPepperIntent".equals(intentName)) {
            if (intent.getSlot("cmd") != null && intent.getSlot("cmd").getValue() != null) {
                cmd = intent.getSlot("cmd").getValue().toLowerCase();
            } else {
                cmd = "unbekannter roboter";
            }

            if (intent.getSlot("action") != null && intent.getSlot("action").getValue() != null) {
                action = intent.getSlot("action").getValue().toLowerCase();
            } else {
                action = "unbekannte aktion";
            }
        }

        if ("GetNewPepperIntent".equals(intentName)) {
            return getNewPepperResponse(action, cmd);

        } else if ("AMAZON.HelpIntent".equals(intentName)) {
            return getHelpResponse();

        } else if ("AMAZON.StopIntent".equals(intentName)) {
            PlainTextOutputSpeech outputSpeech = new PlainTextOutputSpeech();
            outputSpeech.setText("Goodbye");
            return SpeechletResponse.newTellResponse(outputSpeech);
        } else if ("AMAZON.CancelIntent".equals(intentName)) {
            PlainTextOutputSpeech outputSpeech = new PlainTextOutputSpeech();
            outputSpeech.setText("Goodbye");
            return SpeechletResponse.newTellResponse(outputSpeech);
        } else {
            throw new SpeechletException("Invalid Intent");
        }
    }

    @Override
    public void onSessionEnded(final SessionEndedRequest request, final Session session) throws SpeechletException {
        log.info("onSessionEnded requestId={}, sessionId={}", request.getRequestId(), session.getSessionId());
    }

    /**
     * Generate a String response based on the current slots.
     * The mensa plan is provided as JSON on the web.
     * @return String
     * @param day The desired day of the week
     * @param kind The desired menue, e.g., vital, vegetarian, etc.
     * @throws IOException
     * @see "https://raw.githubusercontent.com/warp1337/ubmensa2json/master/ub_mensa.json"
     */

    /**
     * Generate a response based on the current slots.
     * The mensa plan is provided as JSON on the web.
     * @return SpeechletResponse
     * @param day The desired day of the week
     * @param menue The desired menue, e.g., vital, vegetarian, etc.
     */
    private SpeechletResponse getNewPepperResponse(String action, String cmd) {

        // Actions: befindet, hole, personen, beschäftigt
        // CMD: befindet, hole, personen, beschäftigt

        String speechText = "";
        String speechTextCmd = cmd;
        String speechTextAction = action;

        if ("pepper".equals(speechTextCmd)) {
            if ("befindet".equals(speechTextAction)) {
                //speechText = speechTextCmd+"befindet sich im Wohnzimmer";
                String result = httpClientGet.getContent("http://warp1337.com:5000/tobi/location");
                speechText = result;
            }
            if ("personen".equals(speechTextAction)) {
                //speechText = speechTextCmd+"sieht vier personen";
                String result = httpClientGet.getContent("http://warp1337.com:5000/tobi/numberOfPersons");
                speechText = result;
            }
            if ("beschäftigt".equals(speechTextAction)) {
                speechText = "Nein, er schaut Netflix";
                // String result = httpClientGet.getContent("http://warp1337.com:5000/tobi/busy");
            }
            if ("hole".equals(speechTextAction)) {
                speechText = "Ich versuche"+speechTextCmd+"zu holen";
            }
        }

        if ("tobi".equals(speechTextCmd)) {
            if ("befindet".equals(speechTextAction)) {
                String result = httpClientGet.getContent("http://warp1337.com:5000/tobi/location");
                speechText = result;
            }
            if ("personen".equals(speechTextAction)) {
                String result = httpClientGet.getContent("http://warp1337.com:5000/tobi/numberOfPersons");
                speechText = result;
            }
            if ("beschäftigt".equals(speechTextAction)) {
                speechText = "Nein, er schaut Netflix";
                // String result = httpClientGet.getContent("http://warp1337.com:5000/tobi/busy");
            }
            if ("hole".equals(speechTextAction)) {
                speechText = "Ich versuche"+speechTextCmd+"zu holen";
            }
        }

        SimpleCard card = new SimpleCard();
        card.setTitle("Pepper");
        card.setContent(speechText);

        PlainTextOutputSpeech speech = new PlainTextOutputSpeech();
        speech.setText(speechText);

        return SpeechletResponse.newTellResponse(speech, card);
    }

    /**
     * Generate a static help response
     * @return SpeechletResponse
     */
    private SpeechletResponse getHelpResponse() {
        String speechText = "Du kannst fragen welche Menues es heute in der Mensa der Universitaet Bielefeld gibt. Frage zum Beispiel: Mensa Bielefeld Heute Tagesmenue";

        PlainTextOutputSpeech speech = new PlainTextOutputSpeech();
        speech.setText(speechText);

        Reprompt reprompt = new Reprompt();
        reprompt.setOutputSpeech(speech);

        return SpeechletResponse.newAskResponse(speech, reprompt);
    }

    /**
     * Generate a static welcome response
     * @return SpeechletResponse
     */
    private SpeechletResponse getNewWelcomeResponse() {
        String speechText = "OK";

        PlainTextOutputSpeech speech = new PlainTextOutputSpeech();
        speech.setText(speechText);

        Reprompt reprompt = new Reprompt();
        reprompt.setOutputSpeech(speech);

        return SpeechletResponse.newAskResponse(speech, reprompt);
    }
}