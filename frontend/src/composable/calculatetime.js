export function timeSince(date) {
    const seconds = Math.floor((new Date() - new Date(date)) / 1000);

    if (seconds < 0) {
        return "미래";
    }

    const intervals = [
        { seconds: 31536000, label: "년" },
        { seconds: 2592000, label: "달" },
        { seconds: 604800, label: "주" },
        { seconds: 86400, label: "일" },
        { seconds: 3600, label: "시간" },
        { seconds: 60, label: "분" }
    ];

    for (let i = 0; i < intervals.length; i++) {
        const interval = Math.floor(seconds / intervals[i].seconds);
        if (interval >= 1) {
            return `${interval}${intervals[i].label} 전`;
        }
    }

    return "방금 전";
}
