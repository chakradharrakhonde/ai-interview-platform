'use client';

import React, { useState } from 'react';
import { Button, Card, showNotification } from './common';
import { resumeAPI } from '@/lib/api';

interface ResumeData {
  id?: string;
  file_name: string;
  ats_score?: number;
  feedback?: string;
  skills?: string[];
}

export default function ResumeUploader() {
  const [resume, setResume] = useState<ResumeData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isScoring, setIsScoring] = useState(false);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    try {
      const response = await resumeAPI.upload(file);
      setResume({
        id: response.data.id,
        file_name: response.data.file_name,
      });
      showNotification('Resume uploaded successfully!');
    } catch (error: any) {
      showNotification(error.response?.data?.detail || 'Upload failed', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleScoreResume = async () => {
    if (!resume?.id) return;
    
    setIsScoring(true);
    try {
      const response = await resumeAPI.scoreResume(resume.id);
      setResume({
        ...resume,
        ats_score: response.data.ats_score,
        feedback: response.data.feedback,
        skills: response.data.skills,
      });
      showNotification('Resume scored successfully!');
    } catch (error: any) {
      showNotification(error.response?.data?.detail || 'Scoring failed', 'error');
    } finally {
      setIsScoring(false);
    }
  };

  return (
    <Card className="w-full">
      <h3 className="text-xl font-bold mb-4">Resume Uploader</h3>
      
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">Upload Resume</label>
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleFileUpload}
          disabled={isLoading}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
      </div>

      {resume && (
        <div className="space-y-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm font-medium text-gray-600">Uploaded File:</p>
            <p className="text-lg font-semibold text-gray-900">{resume.file_name}</p>
          </div>
          
          {resume.ats_score ? (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">ATS Score:</span>
                <span className="text-2xl font-bold text-green-600">{resume.ats_score}%</span>
              </div>
              {resume.feedback && (
                <p className="text-sm text-gray-700">{resume.feedback}</p>
              )}
              {resume.skills && resume.skills.length > 0 && (
                <div>
                  <p className="text-sm font-medium mb-2">Skills Detected:</p>
                  <div className="flex flex-wrap gap-2">
                    {resume.skills.map((skill, i) => (
                      <span key={i} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <Button onClick={handleScoreResume} isLoading={isScoring} className="w-full">
              Get ATS Score
            </Button>
          )}
        </div>
      )}
    </Card>
  );
}
