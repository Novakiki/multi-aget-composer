'use client';

import * as React from 'react';

interface ViewToggleProps {
    view: 'individual' | 'shared' | 'system';
    onViewChange: (view: 'individual' | 'shared' | 'system') => void;
}

export function ViewToggle({ view, onViewChange }: ViewToggleProps) {
    return (
        <div className="flex gap-2 mb-4 p-2 bg-gray-100 rounded-lg">
            <button
                type="button"
                onClick={() => onViewChange('individual')}
                className={`flex-1 py-2 px-4 rounded-md transition-colors ${
                    view === 'individual'
                        ? 'bg-white shadow text-indigo-700'
                        : 'text-gray-600 hover:bg-gray-200'
                }`}
            >
                <span className="block text-sm font-medium">Your Understanding</span>
                <span className="text-xs">Personal Insights</span>
            </button>
            <button
                type="button"
                onClick={() => onViewChange('shared')}
                className={`flex-1 py-2 px-4 rounded-md transition-colors ${
                    view === 'shared'
                        ? 'bg-white shadow text-green-700'
                        : 'text-gray-600 hover:bg-gray-200'
                }`}
            >
                <span className="block text-sm font-medium">Shared Understanding</span>
                <span className="text-xs">Group Insights</span>
            </button>
            <button
                type="button"
                onClick={() => onViewChange('system')}
                className={`flex-1 py-2 px-4 rounded-md transition-colors ${
                    view === 'system'
                        ? 'bg-white shadow text-blue-700'
                        : 'text-gray-600 hover:bg-gray-200'
                }`}
            >
                <span className="block text-sm font-medium">System View</span>
                <span className="text-xs">How It Works</span>
            </button>
        </div>
    );
} 