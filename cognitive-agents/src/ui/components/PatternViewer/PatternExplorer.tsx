'use client';

import * as React from 'react';
import type { Pattern } from '../../types/components';
import { useState } from 'react';
import { RelatedPatterns } from './RelatedPatterns';
import { RealWorldExample } from './RealWorldExample';
import { AlgorithmExplanation } from './AlgorithmExplanation';
import { ViewToggle } from './ViewToggle';
import { ConnectionLines } from './ConnectionLines';
import { PatternInfluences } from './PatternInfluences';

interface PatternExplorerProps {
    pattern: Pattern;
    onThemeClick: (theme: string) => void;
}

export function PatternExplorer({ pattern, onThemeClick }: PatternExplorerProps) {
    const [activeTheme, setActiveTheme] = useState<string | null>(null);
    const [themeDetails, setThemeDetails] = useState<{
        relatedPatterns: number;
        strength: number;
        description: string;
    } | null>(null);
    const [relatedPatterns, setRelatedPatterns] = useState<Pattern[]>([]);
    const [currentView, setCurrentView] = useState<'outside' | 'inside'>('outside');

    const handleThemeClick = async (theme: string) => {
        setActiveTheme(theme);
        onThemeClick(theme);
        
        // Simulate fetching theme details (replace with actual API call)
        setThemeDetails({
            relatedPatterns: Math.floor(Math.random() * 10) + 1,
            strength: Math.random(),
            description: `Theme "${theme}" represents a key pattern in understanding evolution.`
        });

        // Simulate fetching related patterns (replace with actual API call)
        setRelatedPatterns([
            {
                id: 'related-1',
                content: 'Patterns emerge through natural connections',
                themes: [theme, 'emergence', 'natural'],
                confidence: 0.85,
                evolution: {
                    stage: 'established',
                    history: [{
                        stage: 'initial',
                        timestamp: '2024-01-01T00:00:00.000Z',
                        changes: [{
                            type: 'creation',
                            description: 'Pattern discovered'
                        }]
                    }]
                },
                connections: []
            },
            {
                id: 'related-2',
                content: 'Understanding deepens through exploration',
                themes: [theme, 'understanding', 'depth'],
                confidence: 0.75,
                evolution: {
                    stage: 'developing',
                    history: [{
                        stage: 'initial',
                        timestamp: '2024-01-01T00:00:00.000Z',
                        changes: [{
                            type: 'creation',
                            description: 'Pattern emerged'
                        }]
                    }]
                },
                connections: []
            }
        ]);
    };

    return (
        <div className="mt-4 border-t pt-4">
            <ViewToggle view={currentView} onViewChange={setCurrentView} />
            
            {currentView === 'outside' && (
                <>
                    <h3 className="text-lg font-semibold text-gray-800 mb-3">
                        Explore Patterns (The Outside View)
                    </h3>
                    
                    {/* Theme Explorer with Active State */}
                    <div className="mb-4">
                        <h4 className="font-medium text-gray-700 mb-2">Theme Connections:</h4>
                        <div className="flex gap-2">
                            {pattern.themes.map((theme) => (
                                <button
                                    key={theme}
                                    type="button"
                                    onClick={() => handleThemeClick(theme)}
                                    className={`px-3 py-1 rounded-full text-sm font-medium
                                             transition-colors duration-200 ${
                                        activeTheme === theme 
                                            ? 'bg-indigo-600 text-white' 
                                            : 'bg-indigo-100 hover:bg-indigo-200 text-indigo-700'
                                    }`}
                                >
                                    {theme}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Add Theme Details Panel */}
                    {activeTheme && themeDetails && (
                        <div className="mt-4 p-4 border border-indigo-100 rounded-lg bg-indigo-50">
                            <h4 className="font-medium text-indigo-900 mb-2">
                                Theme: {activeTheme}
                            </h4>
                            <div className="space-y-2">
                                <p className="text-sm text-indigo-800">
                                    {themeDetails.description}
                                </p>
                                <div className="flex gap-4 text-sm text-indigo-700">
                                    <span>Related Patterns: {themeDetails.relatedPatterns}</span>
                                    <span>Strength: {Math.round(themeDetails.strength * 100)}%</span>
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTheme && relatedPatterns.length > 0 && (
                        <RelatedPatterns 
                            theme={activeTheme}
                            patterns={relatedPatterns}
                            onPatternSelect={(p) => console.log('Selected pattern:', p)}
                        />
                    )}

                    {activeTheme && (
                        <RealWorldExample theme={activeTheme} />
                    )}

                    {/* Evolution Timeline with Better Visualization */}
                    <div>
                        <h4 className="font-medium text-gray-700 mb-2">Pattern Evolution:</h4>
                        <div className="space-y-2">
                            {pattern.evolution.history.map((step, i) => (
                                <div key={`${step.stage}-${i}`} className="flex items-center gap-2">
                                    <div className={`w-2 h-2 rounded-full ${
                                        i === pattern.evolution.history.length - 1 
                                            ? 'bg-indigo-600' 
                                            : 'bg-indigo-300'
                                    }`} />
                                    <span className="text-sm text-gray-600">
                                        {step.stage}: {step.description}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </>
            )}

            <ConnectionLines />

            {currentView === 'inside' && (
                <>
                    <h3 className="text-lg font-semibold text-blue-800 mb-3">
                        Look Under the Hood (The Inside View)
                    </h3>
                    <AlgorithmExplanation />
                </>
            )}
        </div>
    );
} 