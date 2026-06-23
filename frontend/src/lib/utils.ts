export function cn(...classes: (string | undefined | false | null)[]) {
  return classes.filter(Boolean).join(" ");
}
export function fmt(n: number, decimals = 1) {
  return n.toFixed(decimals);
}
export function fmtPct(n: number) {
  return `${n.toFixed(1)}%`;
}
export function evColor(ev: number) {
  if (ev >= 3)  return "text-clr-green";
  if (ev >= 0)  return "text-yellow-400";
  return "text-clr-red";
}
export function confColor(c: number) {
  if (c >= 75) return "#00C853";
  if (c >= 55) return "#FFC107";
  return "#FF5252";
}
