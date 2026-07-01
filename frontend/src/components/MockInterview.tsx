'use client';

import React, { useState, useEffect } from 'react';
import { Button, Card, showNotification } from './common';
import { interviewAPI } from '@/lib/api';

interface Interview {
  id: string;
  type: string;
  status: string;
  score?: number;
}

export default function MockInterview() {
  const [interview, setInterview] = useState<Interview | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answer, setAnswer] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [feedback, setFeedback] = useState<any>(null);

  const questions = [
    "Tell me about yourself and your experience?",
    "What are your strengths and weaknesses?",
    "Why do you want to work here?",
    "Describe a challenging project you worked on.",
    "How do you handle conflicts in a team?",
  ];

  const startInterview = async () => {
    setIsLoading(true);
    try {
      const response = await interviewAPI.startInterview({
        type: 'behavioral',
        title: 'Behavioral Interview',
        duration_minutes: 30,
      });
      setInterview(response.data);
      setCurrentQuestion(0);
      setAnswer('');
      showNotification('Interview started!');
    } catch (error: any) {
      showNotification(error.response?.data?.detail || 'Failed to start interview', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!interview || !answer.trim()) {
      showNotification('Please provide an answer', 'error');
      return;
    }

    setIsLoading(true);
    try {
      const response = await interviewAPI.submitAnswer(interview.id, {
        question_number: currentQuestion + 1,
        question_text: questions[currentQuestion],
        text_response: answer,
      });
      
      setFeedback(response.data);
      showNotification('Answer submitted! Check feedback.');
      
      if (currentQuestion < questions.length - 1) {
        setTimeout(() => {
          setCurrentQuestion(currentQuestion + 1);
          setAnswer('');
          setFeedback(null);
        }, 2000);
      }
    } catch (error: any) {
      showNotification(error.response?.data?.detail || 'Failed to submit answer', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  if (!interview) {
    return (
      <Card className="w-full text-center">
        <h3 className="text-xl font-bold mb-4">Mock Interview</h3>
        <p className="text-gray-600 mb-6">Practice with AI-generated questions and get instant feedback</p>
        <Button onClick={startInterview} isLoading={isLoading} size="lg">
          Start Interview
        </Button>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">Question {currentQuestion + 1} of {questions.length}</h3>
          <div className="w-full bg-gray-200 rounded-full h-2 ml-4">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all"
              style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>
        
        <div className="bg-blue-50 p-4 rounded-lg mb-6">
          <p className="text-lg text-gray-900">{questions[currentQuestion]}</p>
        </div>
        
        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type your answer here..."
          className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {feedback && (
          <div className="mt-4 bg-green-50 p-4 rounded-lg">
            <p className="font-semibold text-green-900 mb-2">Feedback:</p>
            <p className="text-green-800">{feedback.feedback}</p>
            <p className="mt-2 text-sm text-green-700">Score: {feedback.score}/100</p>
          </div>
        )}

        <div className="flex gap-4 mt-6">
          <Button onClick={submitAnswer} isLoading={isLoading} className="flex-1">
            Submit Answer
          </Button>
          {currentQuestion < questions.length - 1 && (
            <Button
              variant="outline"
              onClick={() => {
                setCurrentQuestion(currentQuestion + 1);
                setAnswer('');
                setFeedback(null);
              }}
              className="flex-1"
            >
              Skip
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
}
