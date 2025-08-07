export function Input({ type = "text", className = "", ...props }) {
    return (
        <input
            type={type}
            className={`border rounded-xl p-2 w-full ${className}`}
            {...props}
        />
    );
}
