export default function Header() {
  return (
    <header className="bg-white shadow px-6 py-4 flex items-center justify-between">
      <h1 className="text-xl font-semibold text-gray-800">
        {/* El título se actualizará dinámicamente más adelante */}
        Panel de Administración
      </h1>
      <div className="flex items-center gap-3">
        <span className="text-gray-600">Admin</span>
        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
          A
        </div>
      </div>
    </header>
  );
}