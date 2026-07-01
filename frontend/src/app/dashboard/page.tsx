'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { Card, Button, showNotification } from '@/components/common';
import { dashboardAPI } from '@/lib/api';

interface Stats {
  total_interviews: number;
  average_score: number;
  total_resumes: number;
  latest_resume_score: number | null;
}

export default function DashboardPage() {
  const { isAuthenticated, user } = useAuthStore();
  const router = useRouter();
  const [stats, setStats] = useState<Stats | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    fetchStats();
  }, [isAuthenticated]);

  const fetchStats = async () => {
    try {
      const response = await dashboardAPI.getStats();
      setStats(response.data);
    } catch (error: any) {
      showNotification(error.response?.data?.detail || 'Failed to load stats', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Welcome, {user?.first_name || user?.email}!</h1>
        <p className="text-gray-600">Track your progress and improve your interview skills</p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Loading...</p>
        </div>
      ) : (
        <>
          <div className="grid md:grid-cols-4 gap-6 mb-12">
            <Card>
              <p className="text-gray-600 text-sm">Total Interviews</p>
              <p className="text-3xl font-bold text-blue-600 mt-2">{stats?.total_interviews || 0}</p>
            </Card>
            <Card>
              <p className="text-gray-600 text-sm">Average Score</p>
              <p className="text-3xl font-bold text-green-600 mt-2">{Math.round(stats?.average_score || 0)}%</p>
            </Card>
            <Card>
              <p className="text-gray-600 text-sm">Resumes Uploaded</p>
              <p className="text-3xl font-bold text-purple-600 mt-2">{stats?.total_resumes || 0}</p>
            </Card>
            <Card>
              <p className="text-gray-600 text-sm">Latest ATS Score</p>
              <p className="text-3xl font-bold text-orange-600 mt-2">
                {stats?.latest_resume_score ? Math.round(stats.latest_resume_score) : 'N/A'}
              </p>
            </Card>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <Card className="text-center">
              <h3 className="text-xl font-bold mb-4">Practice Interviews</h3>
              <p className="text-gray-600 mb-6">Take mock interviews and get instant feedback</p>
              <Button onClick={() => router.push('/interview')} className="w-full">
                Start Interview
              </Button>
            </Card>
            <Card className="text-center">
              <h3 className="text-xl font-bold mb-4">Upload Resume</h3>
              <p className="text-gray-600 mb-6">Get ATS scoring and improvement suggestions</p>
              <Button onClick={() => router.push('/resume')} className="w-full">
                Upload Resume
              </Button>
            </Card>
            <Card className="text-center">
              <h3 className="text-xl font-bold mb-4">Coding Practice</h3>
              <p className="text-gray-600 mb-6">Practice coding problems by difficulty level</p>
              <Button onClick={() => router.push('/coding')} className="w-full">
                Start Coding
              </Button>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}
