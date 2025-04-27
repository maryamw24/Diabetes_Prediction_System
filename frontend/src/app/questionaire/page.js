'use client';

import { useState } from 'react';
import ResultDisplay from '../../../components/ResultDisplay';

const questions = [
  { key: "Age", question: "What is your age?", type: "number" },
  { key: "Gender", question: "What is your gender?", type: "select", options: ["Male", "Female"] },
  { key: "Polyuria", question: "Do you experience frequent urination?", type: "boolean" },
  { key: "Polydipsia", question: "Do you feel excessive thirst?", type: "boolean" },
  { key: "sudden_weight_loss", question: "Have you experienced sudden weight loss?", type: "boolean" },
  { key: "weakness", question: "Do you often feel weak?", type: "boolean" },
  { key: "Polyphagia", question: "Do you feel excessive hunger?", type: "boolean" },
  { key: "Genital_thrush", question: "Do you suffer from genital thrush?", type: "boolean" },
  { key: "visual_blurring", question: "Do you experience blurred vision?", type: "boolean" },
  { key: "Itching", question: "Do you experience frequent itching?", type: "boolean" },
  { key: "Irritability", question: "Do you feel unusually irritable?", type: "boolean" },
  { key: "delayed_healing", question: "Do your wounds take longer to heal?", type: "boolean" },
  { key: "partial_paresis", question: "Do you experience partial muscle weakness?", type: "boolean" },
  { key: "muscle_stiffness", question: "Do you suffer from muscle stiffness?", type: "boolean" },
  { key: "Alopecia", question: "Have you noticed unusual hair loss (Alopecia)?", type: "boolean" },
  { key: "Obesity", question: "Are you classified as obese?", type: "boolean" },
];

export default function Questionnaire() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  const handleAnswer = (value) => {
    const key = questions[currentQuestion].key;
    let booleanValue = value;
    if(value === "Yes" || value === "No") {
          booleanValue = value === "Yes" ? 1 : value === "No" ? 0 : value;
    }
    else if (value === 'Male' || value === 'Female') {
          booleanValue = value === "Male" ? 1 : value === "Female" ? 0 : value;
    }
    setAnswers({ ...answers, [key]: booleanValue });

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      console.log("Final Answers:", { ...answers, [key]: booleanValue });
      submitAnswers({ ...answers, [key]: booleanValue });
    }
  };

  const submitAnswers = async (finalAnswers) => {
    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(finalAnswers),
      });

      const data = await response.json();
      console.log("Response from server:", data);
      setResult(data);
    } catch (error) {
      console.error("Error submitting data:", error);
    }
  };

  const question = questions[currentQuestion];

  return (
    <div className="flex flex-col items-center justify-center h-screen p-4 bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md text-center">
        {result ? (
          <ResultDisplay result={result} />
        ) : (
          <>
            <h2 className="text-xl text-black font-semibold mb-4">{question.question}</h2>

            {question.type === "boolean" && (
              <div className="flex justify-around">
                <button
                  onClick={() => handleAnswer("Yes")}
                  className="bg-green-500 text-black px-4 py-2 rounded hover:bg-green-600"
                >
                  Yes
                </button>
                <button
                  onClick={() => handleAnswer("No")}
                  className="bg-red-500 text-black px-4 py-2 rounded hover:bg-red-600"
                >
                  No
                </button>
              </div>
            )}

            {question.type === "select" && (
              <div className="flex flex-col gap-2">
                {question.options.map((option) => (
                  <button
                    key={option}
                    onClick={() => handleAnswer(option)}
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                  >
                    {option}
                  </button>
                ))}
              </div>
            )}

            {question.type === "number" && (
              <div className="flex flex-col gap-2">
                <input
                  type="number"
                  onChange={(e) => setAnswers({ ...answers, [question.key]: e.target.value })}
                  className="border text-black p-2 rounded"
                />
                <button
                  onClick={() => {
                    if (answers[question.key]) setCurrentQuestion(currentQuestion + 1);
                  }}
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
