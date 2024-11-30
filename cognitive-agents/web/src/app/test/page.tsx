'use client';

import React from 'react';
import { PatternViewer } from '@/components/PatternViewer';
import type { Pattern } from '@/types/components';

// Test data matching our Pattern type
const testPattern: Pattern = {
    id: "test-1",
    content: "Test pattern for visualization",
    themes: ["testing", "visualization", "ui"],
    confidence: 0.8,
    evolution: {
        stage: "developing",
        history: [{
            stage: "initial",
            timestamp: new Date('2024-01-01T00:00:00.000Z'),
            changes: [{
                type: "creation" as const,
                description: "Initial pattern creation",
                before: undefined,
                after: undefined
            }]
        }]
    },
    connections: []
};

export default function TestPage() {
    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-8">Pattern Viewer Test</h1>
            <PatternViewer pattern={testPattern} />
        </div>
    );
}