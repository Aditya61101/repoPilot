interface Label {
    color: string;
    name: string;
}
export interface Issue {
    id: number;
    title: string;
    state: string;
    createdAt: string;
    labels?: Label[];
    body: string;
}

export interface Repo {
    id: string;
    name: string;
}