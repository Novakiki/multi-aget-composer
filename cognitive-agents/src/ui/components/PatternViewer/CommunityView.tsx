'use client';

import * as React from 'react';
import type { Pattern } from '../../types/components';

interface CommunityViewProps {
    pattern: Pattern;
}

export function CommunityView({ pattern }: CommunityViewProps) {
    return (
        <div className="space-y-4">
            <div className="p-4 bg-green-50 rounded-lg border border-green-100">
                <h4 className="font-medium text-green-900 mb-3">Community Insights</h4>
                
                {/* Community Stats */}
                <div className="grid grid-cols-3 gap-4 mb-4">
                    <div className="p-3 bg-white rounded-lg">
                        <span className="block text-sm text-green-600">People Exploring</span>
                        <span className="text-2xl font-bold text-green-700">24</span>
                    </div>
                    <div className="p-3 bg-white rounded-lg">
                        <span className="block text-sm text-green-600">Related Questions</span>
                        <span className="text-2xl font-bold text-green-700">12</span>
                    </div>
                    <div className="p-3 bg-white rounded-lg">
                        <span className="block text-sm text-green-600">Pattern Strength</span>
                        <span className="text-2xl font-bold text-green-700">85%</span>
                    </div>
                </div>

                {/* Community Questions */}
                <div className="space-y-2">
                    <h5 className="font-medium text-green-800">Active Questions:</h5>
                    <ul className="space-y-2">
                        <li className="p-2 bg-white rounded">
                            "How do these patterns evolve naturally?"
                        </li>
                        <li className="p-2 bg-white rounded">
                            "What connects these patterns?"
                        </li>
                    </ul>
                </div>
            </div>

            {/* Collective Understanding */}
            <div className="p-4 bg-green-50 rounded-lg border border-green-100">
                <h4 className="font-medium text-green-900 mb-3">Collective Understanding</h4>
                <div className="space-y-3">
                    <p className="text-green-700">
                        The community is discovering how patterns naturally connect and evolve.
                    </p>
                    <div className="flex gap-2">
                        {pattern.themes.map(theme => (
                            <span 
                                key={theme}
                                className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-sm"
                            >
                                {theme}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
} 