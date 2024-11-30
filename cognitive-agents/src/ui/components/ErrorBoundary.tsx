import * as React from 'react';
import { PatternError } from '@/types';

interface Props {
    children: React.ReactNode;
    fallback?: React.ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
}

export class ErrorBoundary extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    render() {
        if (this.state.hasError) {
            if (this.props.fallback) {
                return this.props.fallback;
            }

            return (
                <div className="p-4 bg-red-50 border border-red-100 rounded-lg">
                    <h3 className="text-lg font-medium text-red-800 mb-2">
                        Something went wrong
                    </h3>
                    <p className="text-sm text-red-600">
                        {this.state.error instanceof PatternError 
                            ? this.state.error.message
                            : 'An unexpected error occurred'}
                    </p>
                </div>
            );
        }

        return this.props.children;
    }
} 