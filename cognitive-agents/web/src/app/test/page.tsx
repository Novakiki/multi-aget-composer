'use client';

import dynamic from 'next/dynamic';
import type { Pattern } from '@/types/components';

// Import PatternViewer with no SSR and loading state
const PatternViewer = dynamic(
    () => import('@/components/PatternViewer').then(mod => mod.PatternViewer),
    { 
        ssr: false,
        loading: () => <div className="p-4 border rounded-lg shadow-sm">Loading...</div>
    }
);

// Move test data to a constant to prevent re-creation
const TEST_PATTERN: Pattern = {
    id: "test-1",
    content: "Test pattern for visualization",
    themes: ["testing", "visualization", "ui"],
    confidence: 0.8,
    evolution: {
        stage: "developing",
        history: [{
            stage: "initial",
            timestamp: "2024-01-01T00:00:00.000Z",  // Use string instead of Date
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
            <PatternViewer pattern={TEST_PATTERN} />
        </div>
    );
}