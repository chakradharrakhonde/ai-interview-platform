'use client';

import React, { useState } from 'react';
import { useAuthStore } from '@/lib/store';
import { useRouter } from 'next/navigation';
import { Card, Button, Input, showNotification } from '@/components/common';
import { codingAPI } from '@/lib/api';

interface CodingQuestion {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  topic: string;
  time_limit_minutes: number;
}

export default function CodingPage() {
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();
  const [questions, setQuestions] = useState<CodingQuestion[]>([]);
  const [selectedQuestion, setSelectedQuestion] = useState<CodingQuestion | null>(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  if (!isAuthenticated) {
    router.push('/auth/login');
    return null;
  }

  const loadQuestions = async (difficulty: string) => {
    setIsLoading(true);
    try {
      const response = await codingAPI.getQuestions(difficulty);
      setQuestions(response.data);
    } catch (error: any) {
      showNotification(error.response?.data?.detail || 'Failed to load questions', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const submitCode = async () => {
    if (!selectedQuestion || !code.trim()) {
      showNotification('Please select a question and write code', 'error');
      return;
    }

    setIsLoading(true);
    try {
      const response = await codingAPI.submitCode({
        code,
        language,
        question_id: selectedQuestion.id,
      });
      setResult(response.data);
      showNotification(response.data.passed ? 'All tests passed!' : 'Some tests failed');
    } catch (error: any) {
      showNotification(error.response?.data?.detail || 'Failed to submit code', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Coding Practice</h1>

      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <Button onClick={() => loadQuestions('easy')} className="w-full">
          Easy Questions
        </Button>
        <Button onClick={() => loadQuestions('medium')} className="w-full">
          Medium Questions
        </Button>
        <Button onClick={() => loadQuestions('hard')} className="w-full">
          Hard Questions
        </Button>
      </div>

      {questions.length > 0 && (
        <div className="grid md:grid-cols-4 gap-6">
          <div className="md:col-span-1">
            <Card>
              <h3 className="font-bold mb-4">Questions</h3>
              <div className="space-y-2">
                {questions.map((q) => (
                  <button
                    key={q.id}
                    onClick={() => setSelectedQuestion(q)}
                    className={`w-full text-left p-2 rounded ${
                      selectedQuestion?.id === q.id
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 hover:bg-gray-200'
                    }`}
                  >
                    <p className="font-semibold text-sm">{q.title}</p>
                    <p className="text-xs text-gray-600">{q.difficulty}</p>
                  </button>
                ))}
              </div>
            </Card>
          </div>

          <div className="md:col-span-3">
            {selectedQuestion && (
              <div className="space-y-6">
                <Card>
                  <h3 className="text-2xl font-bold mb-4">{selectedQuestion.title}</h3>
                  <p className="text-gray-600 mb-4">{selectedQuestion.description}</p>
                  <div className="flex gap-4 text-sm text-gray-600">
                    <span>Difficulty: <strong>{selectedQuestion.difficulty}</strong></span>
                    <span>Time: <strong>{selectedQuestion.time_limit_minutes}m</strong></span>
                  </div>
                </Card>

                <Card>
                  <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">Language</label>
                    <select
                      value={language}
                      onChange={(e) => setLanguage(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                    >
                      <option value="python">Python</option>
                      <option value="javascript">JavaScript</option>
                      <option value="java">Java</option>
                      <option value="cpp">C++</option>
                    </select>
                  </div>
                  
                  <label className="block text-sm font-medium mb-2">Code</label>
                  <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="Write your solution here..."
                    className="w-full h-64 p-4 border border-gray-300 rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  
                  <Button onClick={submitCode} isLoading={isLoading} className="w-full mt-4">
                    Submit Solution
                  </Button>
                </Card>

                {result && (
                  <Card className={result.passed ? 'bg-green-50' : 'bg-red-50'}>
                    <h4 className="font-bold mb-4">
                      {result.passed ? '✅ All Tests Passed!' : '❌ Some Tests Failed'}
                    </h4>
                    <p className="text-gray-700 mb-4">{result.feedback}</p>
                    <p className="font-semibold">Score: {result.score}/100</p>
                    {result.test_results && (
                      <div className="mt-4">
                        <h5 className="font-semibold mb-2">Test Results:</h5>
                        <div className="space-y-2">
                          {result.test_results.map((test: any, i: number) => (
                            <p key={i} className="text-sm">
                              {test.passed ? '✅' : '❌'} {test.test}
                            </p>
                          ))}
                        </div>
                      </div>
                    )}
                  </Card>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
