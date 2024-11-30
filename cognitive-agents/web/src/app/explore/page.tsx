'use client';

import dynamic from 'next/dynamic';
import type { Pattern } from '@/types';

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
            <h1 className="text-2xl font-bold mb-8">
                Pattern Evolution Space
                <span className="ml-2 text-sm text-indigo-600">
                    Explore & Learn Together
                </span>
            </h1>
            
            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Left: Pattern Viewer with all three views */}
                <div>
                    <PatternViewer pattern={TEST_PATTERN} />
                </div>

                {/* Right: Interaction Space */}
                <div className="space-y-6">
                    <InteractionSpace />
                    
                    {/* Quick Actions */}
                    <div className="p-4 bg-gray-50 rounded-lg">
                        <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
                        <div className="space-y-2">
                            <button 
                                type="button"
                                className="w-full p-2 bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200"
                            >
                                Ask a Question
                            </button>
                            <button 
                                type="button"
                                className="w-full p-2 bg-green-100 text-green-700 rounded hover:bg-green-200"
                            >
                                Share an Insight
                            </button>
                            <button 
                                type="button"
                                className="w-full p-2 bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                            >
                                Explore Patterns
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
} 