export function Input({ type = "text", ...props }) {
    return <input type={type} className="border rounded-xl p-2 w-full" {...props} />;
}