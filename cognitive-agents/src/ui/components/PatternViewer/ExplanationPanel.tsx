'use client';

import * as React from 'react';

export function ExplanationPanel() {
    return (
        <div className="mb-6 p-4 bg-indigo-50 rounded-lg">
            <h3 className="text-lg font-semibold text-indigo-900 mb-2">Understanding Pattern Evolution</h3>
            <div className="space-y-3">
                <div>
                    <h4 className="font-medium text-indigo-800">What You're Seeing:</h4>
                    <ul className="list-disc list-inside text-indigo-700">
                        <li>Content: The raw pattern being analyzed</li>
                        <li>Themes: Natural connections the system discovered</li>
                        <li>Confidence: How strongly the pattern is established</li>
                    </ul>
                </div>
                <div>
                    <h4 className="font-medium text-indigo-800">Behind the Algorithm:</h4>
                    <ul className="list-disc list-inside text-indigo-700">
                        <li>Neo4j: Stores pattern relationships</li>
                        <li>MongoDB: Tracks pattern evolution</li>
                        <li>Pinecone: Handles semantic understanding</li>
                    </ul>
                </div>
            </div>
        </div>
    );
} 