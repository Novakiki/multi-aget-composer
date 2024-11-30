'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import { TEST_PATTERNS } from './testData';
import type { Connection } from '@/types';

const PatternViewer = dynamic(
    () => import('@/components/PatternViewer').then(mod => mod.PatternViewer),
    { ssr: false }
);

export default function TestPage() {
    const [activePattern] = useState(TEST_PATTERNS.main);
    const [activeConnection, setActiveConnection] = useState<string | null>(null);

    const handleThemeExplore = async (theme: string) => {
        console.log(`Exploring theme: ${theme}`);
        // Simulate finding related patterns
        const related = TEST_PATTERNS.related.filter(p => 
            p.themes.includes(theme)
        );
        console.log('Related patterns:', related);
    };

    const handleConnectionExplore = (connectionId: string) => {
        console.log(`Exploring connection: ${connectionId}`);
        setActiveConnection(connectionId);
        // Find connected pattern
        const connection = activePattern.connections.find((c: Connection) => 
            c.connectionId === connectionId
        );
        if (connection) {
            const relatedPattern = TEST_PATTERNS.related.find(p => 
                p.id === connection.targetId
            );
            console.log('Connected pattern:', relatedPattern);
        }
    };

    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-8">
                Pattern Network Test
                <span className="ml-2 text-sm text-gray-500">
                    (Development & Testing)
                </span>
            </h1>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Main Pattern View */}
                <PatternViewer 
                    pattern={activePattern}
                    onThemeClick={handleThemeExplore}
                    onConnectionExplore={handleConnectionExplore}
                />

                {/* Debug Panel */}
                <div className="p-4 bg-gray-50 rounded-lg">
                    <h2 className="text-lg font-semibold mb-4">Debug Info</h2>
                    <pre className="whitespace-pre-wrap text-sm">
                        {JSON.stringify({
                            activePattern: activePattern.id,
                            activeConnection,
                            connectionCount: activePattern.connections.length,
                            themeCount: activePattern.themes.length
                        }, null, 2)}
                    </pre>
                </div>
            </div>
        </div>
    );
}