'use client';

import * as React from 'react';
import { useEffect, useState } from 'react';
import type { Pattern } from '@/types';
import { ExplanationPanel } from './ExplanationPanel';
import { PatternExplorer } from './PatternExplorer';
import { ErrorBoundary } from '../ErrorBoundary';

interface PatternViewerProps {
    pattern?: Pattern;
    onPatternSelect?: (pattern: Pattern) => void;
    onThemeClick?: (theme: string) => Promise<void>;
    onConnectionExplore?: (connectionId: string) => void;
}

export function PatternViewer(props: PatternViewerProps) {
    const [isClient, setIsClient] = useState(false);
    const [selectedPattern, setSelectedPattern] = useState<Pattern | null>(null);

    useEffect(() => {
        setIsClient(true);
        if (props.pattern) {
            setSelectedPattern(props.pattern);
        }
    }, [props.pattern]);

    const handleThemeClick = (theme: string) => {
        console.log(`Exploring theme: ${theme}`);
        // TODO: Implement theme exploration
    };

    if (!isClient) {
        return null;
    }

    return (
        <ErrorBoundary>
            <div className="space-y-6">
                <ExplanationPanel />
                
                <div className="p-4 border rounded-lg shadow-sm bg-white">
                    <h2 className="text-lg font-semibold mb-4 text-gray-800">Pattern Viewer</h2>
                    {selectedPattern ? (
                        <div className="space-y-2">
                            <div>
                                <span className="font-medium text-gray-700">Content:</span>
                                <p className="text-gray-600">{selectedPattern.content}</p>
                            </div>
                            <div>
                                <span className="font-medium text-gray-700">Themes:</span>
                                <div className="flex gap-2">
                                    {selectedPattern.themes.map((theme) => (
                                        <span 
                                            key={theme}
                                            className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium"
                                        >
                                            {theme}
                                        </span>
                                    ))}
                                </div>
                            </div>
                            <div>
                                <span className="font-medium text-gray-700">Confidence:</span>
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                    <div 
                                        className="bg-indigo-600 h-2 rounded-full"
                                        style={{ width: `${selectedPattern.confidence * 100}%` }}
                                    />
                                </div>
                            </div>
                        </div>
                    ) : (
                        <p className="text-gray-500">No pattern selected</p>
                    )}
                    {selectedPattern && (
                        <PatternExplorer 
                            pattern={selectedPattern}
                            onThemeClick={handleThemeClick}
                        />
                    )}
                </div>
            </div>
        </ErrorBoundary>
    );
} 