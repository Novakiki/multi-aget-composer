export type ChangeType = 'creation' | 'modification' | 'connection' | 'evolution';

export interface Change {
    type: ChangeType;
    description: string;
    before?: unknown;
    after?: unknown;
}

export interface EvolutionStep {
    stage: string;
    timestamp: string;
    changes: Change[];
}

export interface Evolution {
    stage: string;
    history: EvolutionStep[];
}

export interface Connection {
    connectionId: string;
    type: string;
    strength: number;
    targetId: string;
    description: string;
}

export interface Pattern {
    id: string;
    content: string;
    themes: string[];
    confidence: number;
    evolution: Evolution;
    connections: Connection[];
}

export class PatternError extends Error {
    constructor(message: string, public code: string) {
        super(message);
        this.name = 'PatternError';
    }
}