'use client';

import dynamic from 'next/dynamic';
import type { Pattern } from '@/types/components';

const TEST_PATTERN: Pattern = {
    id: "test-1",
    content: "Test pattern for visualization",
    themes: ["testing", "visualization", "ui"],
    confidence: 0.8,
    evolution: {
        stage: "developing",
        history: [{
            stage: "initial",
            timestamp: "2024-01-01T00:00:00.000Z",
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

const PatternViewer = dynamic(
    () => import('@/components/PatternViewer').then(mod => mod.PatternViewer),
    { ssr: false }
);

const InteractionSpace = dynamic(
    () => import('@/components/InteractionSpace').then(mod => mod.InteractionSpace),
    { ssr: false }
);

export default function ExplorePage() {
    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-8">Pattern Explorer</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <PatternViewer pattern={TEST_PATTERN} />
                <InteractionSpace />
            </div>
        </div>
    );
} 