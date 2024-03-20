        package com.example.myapplication;

        import android.os.AsyncTask;
        import android.os.Bundle;
        import android.view.View;
        import android.widget.EditText;
        import android.widget.TextView;

        import java.util.ArrayList;
        import java.util.List;


        import com.google.ai.client.generativeai.GenerativeModel;
        import com.google.ai.client.generativeai.java.GenerativeModelFutures;
        import com.google.ai.client.generativeai.type.Content;
        import com.google.ai.client.generativeai.type.GenerateContentResponse;
        import com.google.common.util.concurrent.FutureCallback;
        import com.google.common.util.concurrent.Futures;
        import com.google.common.util.concurrent.ListenableFuture;

        import androidx.appcompat.app.AppCompatActivity;

        import org.json.JSONObject;

        import java.io.OutputStream;
        import java.net.HttpURLConnection;
        import java.net.URL;
        import java.util.Scanner;
        import com.google.ai.client.generativeai.*;

        public class MainActivity extends AppCompatActivity {

            String apiKey = "";

            @Override
            protected void onCreate(Bundle savedInstanceState) {
                super.onCreate(savedInstanceState);
                setContentView(R.layout.activity_main);
            }

            public void registerclick(View view) {
                TextView txt3 = findViewById(R.id.textView3);

                // Generate a lock code based on name2
                NameData nameData = generateName();

                // Display the entered lock code in textView3
                txt3.setText(nameData.getLockCode());

                // Send a POST request to update the lock code
                new UpdateLockCodeTask().execute(nameData.getLockCode());
            }

            public void searchbtn(View view) {
                EditText searchEditText = findViewById(R.id.search);
                String searchQuery = searchEditText.getText().toString();
                geminisearch(searchQuery);
            }

            public void geminisearch(String query) {
                TextView txt = findViewById(R.id.searchtxtprint);
                // Replace "YOUR_MODEL_NAME" with the actual GenerativeAI model name
                // For text-only input, use the gemini-pro model
                GenerativeModel gm = new GenerativeModel(/* modelName */ "gemini-pro",
        // Access your API key as a Build Configuration variable (see "Set up your API key" above)
                        /* apiKey */ "");
                GenerativeModelFutures model = GenerativeModelFutures.from(gm);
                Content content = new Content.Builder()
                        .addText(query)
                        .build();

                ListenableFuture<GenerateContentResponse> response = model.generateContent(content);
                Futures.addCallback(response, new FutureCallback<GenerateContentResponse>() {
                    @Override
                    public void onSuccess(GenerateContentResponse result) {
                        String resultText = result.getText();
                        txt.setText(resultText);
                    }
                    @Override
                    public void onFailure(Throwable t) {
                        txt.setText(t.toString());
                    }
                }, this.getMainExecutor());
            }
            private NameData generateName() {
                EditText edittxtname1 = findViewById(R.id.editTextText);
                EditText edittxtname2 = findViewById(R.id.editTextText2);

                String editTextValue1 = edittxtname1.getText().toString();
                String editTextValue2 = edittxtname2.getText().toString();

                return new NameData(editTextValue1, editTextValue2);
            }


            private class UpdateLockCodeTask extends AsyncTask<String, Void, Void> {
                @Override
                protected Void doInBackground(String... params) {
                    String lockCode = params[0];
                    try {
                        // Get the user input for the URL
                        EditText edittxtname1 = findViewById(R.id.editTextText);
                        String editTextValue1 = edittxtname1.getText().toString();

                        // Construct the URL using user input
                        URL url = new URL(editTextValue1);

                        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                        connection.setRequestMethod("POST");
                        connection.setRequestProperty("Content-Type", "application/json");
                        connection.setDoOutput(true);

                        // Create JSON object with lock code
                        JSONObject jsonInput = new JSONObject();
                        jsonInput.put("lock_code", lockCode);

                        // Write JSON to output stream
                        try (OutputStream os = connection.getOutputStream()) {
                            byte[] input = jsonInput.toString().getBytes("utf-8");
                            os.write(input, 0, input.length);
                        }

                        // Get response from the server
                        Scanner scanner = new Scanner(connection.getInputStream());
                        String response = scanner.useDelimiter("\\A").next();
                        scanner.close();
                        // Handle the response as needed

                        connection.disconnect();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    return null;
                }
            }
        }

        class Message {
            public String text;
            // You may need to add other properties based on your use case

            public Message(String text) {
                this.text = text;
            }

            public String getText() {
                return text;
            }
        }
        class NameData {
            public String name;
            public String name2;

            public NameData(String name, String name2) {
                this.name = name;
                this.name2 = name2;
            }

            public String getLockCode() {
                // Return the lock code directly
                return name2;
            }
        }
