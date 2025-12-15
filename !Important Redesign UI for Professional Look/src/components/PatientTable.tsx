const patientData = [
  {
    sep: '0224R0020250V014657',
    mrn: '0138-25-87',
    nama_pasien: 'AN, A2',
    nokartu: '3467247187',
    dpjp: 'DR, B',
    admission_date: '2025-08-27 00:00:00',
    discharge_date: '2025-07-01 00:00:00',
    los: '5',
    kelas_rawat: '1',
    inacbg: 'K-A-17-I',
    birth_date: '2023-12-18 00:00:00',
    birth_weight: '0.0'
  },
  {
    sep: '0224R0020250V014788',
    mrn: '0143-71-79',
    nama_pasien: 'NY, S',
    nokartu: '1630222488',
    dpjp: 'DR, A',
    admission_date: '2025-08-29 00:00:00',
    discharge_date: '2025-07-01 00:00:00',
    los: '4',
    kelas_rawat: '3',
    inacbg: 'B-A-14-I',
    birth_date: '1988-08-24 00:00:00',
    birth_weight: '0.0'
  },
  {
    sep: '0224R0020250V014820',
    mrn: '0093-02-05',
    nama_pasien: 'TN, H',
    nokartu: '1242247325',
    dpjp: 'DR, A',
    admission_date: '2025-08-28 00:00:00',
    discharge_date: '2025-07-01 00:00:00',
    los: '4',
    kelas_rawat: '1',
    inacbg: 'K-A-18-I',
    birth_date: '1990-08-24 00:00:00',
    birth_weight: '0.0'
  },
  {
    sep: '0224R0020250V014930',
    mrn: '0148-09-28',
    nama_pasien: 'NY, SJ',
    nokartu: '1790190042',
    dpjp: 'DR, A',
    admission_date: '2025-08-29 00:00:00',
    discharge_date: '2025-07-01 00:00:00',
    los: '3',
    kelas_rawat: '3',
    inacbg: 'K-A-17-I',
    birth_date: '1948-08-18 00:00:00',
    birth_weight: '0.0'
  },
  {
    sep: '0224R0020250V014985',
    mrn: '0049-17-32',
    nama_pasien: 'TN, Z',
    nokartu: '1402817816',
    dpjp: 'DR, BP',
    admission_date: '2025-08-27 00:00:00',
    discharge_date: '2025-07-01 00:00:00',
    los: '5',
    kelas_rawat: '1',
    inacbg: 'J-4-17-I',
    birth_date: '1972-07-18 00:00:00',
    birth_weight: '0.0'
  },
  {
    sep: '0224R0020250V014885',
    mrn: '0028-65-16',
    nama_pasien: 'AN, DP',
    nokartu: '2255188649',
    dpjp: 'DR, GD',
    admission_date: '2025-08-28 00:00:00',
    discharge_date: '2025-07-01 00:00:00',
    los: '4',
    kelas_rawat: '1',
    inacbg: 'K-A-17-I',
    birth_date: '2015-02-16 00:00:00',
    birth_weight: '0.0'
  },
  {
    sep: '0224R0020250V014930',
    mrn: '0028-69-29',
    nama_pasien: 'AN, R5L',
    nokartu: '3544829948',
    dpjp: 'DR, GD',
    admission_date: '2025-08-26 00:00:00',
    discharge_date: '2025-07-01 00:00:00',
    los: '6',
    kelas_rawat: '1',
    inacbg: 'K-A-17-I',
    birth_date: '2019-07-26 00:00:00',
    birth_weight: '0.0'
  },
  {
    sep: '0224R0020250V014955',
    mrn: '0138-47-29',
    nama_pasien: 'AN, ARR',
    nokartu: '3566927768',
    dpjp: 'DR, FN',
    admission_date: '2025-08-26 00:00:00',
    discharge_date: '2025-07-01 00:00:00',
    los: '3',
    kelas_rawat: '1',
    inacbg: 'M-4-12-I',
    birth_date: '2024-01-03 00:00:00',
    birth_weight: '0.0'
  }
];

export function PatientTable() {
  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white">
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">SEP</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">MRN</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">NAMA_PASIEN</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">NOKARTU</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">DPJP</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">ADMISSION_DATE</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">DISCHARGE_DATE</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">LOS</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">KELAS_RAWAT</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">INACBG</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">BIRTH_DATE</th>
            <th className="px-4 py-4 text-left text-sm font-semibold whitespace-nowrap">BIRTH_WEIGHT</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {patientData.map((patient, index) => (
            <tr 
              key={index}
              className="hover:bg-blue-50/50 transition-colors"
            >
              <td className="px-4 py-4 text-sm text-gray-900 whitespace-nowrap">{patient.sep}</td>
              <td className="px-4 py-4 text-sm text-gray-900 whitespace-nowrap">{patient.mrn}</td>
              <td className="px-4 py-4 text-sm text-gray-900 whitespace-nowrap">{patient.nama_pasien}</td>
              <td className="px-4 py-4 text-sm text-gray-900 whitespace-nowrap">{patient.nokartu}</td>
              <td className="px-4 py-4 text-sm text-gray-900 whitespace-nowrap">{patient.dpjp}</td>
              <td className="px-4 py-4 text-sm text-gray-600 whitespace-nowrap">{patient.admission_date}</td>
              <td className="px-4 py-4 text-sm text-gray-600 whitespace-nowrap">{patient.discharge_date}</td>
              <td className="px-4 py-4 text-sm whitespace-nowrap">
                <span className="inline-flex items-center px-2.5 py-1 rounded-lg bg-blue-100 text-blue-700">
                  {patient.los}
                </span>
              </td>
              <td className="px-4 py-4 text-sm whitespace-nowrap">
                <span className="inline-flex items-center px-2.5 py-1 rounded-lg bg-cyan-100 text-cyan-700">
                  {patient.kelas_rawat}
                </span>
              </td>
              <td className="px-4 py-4 text-sm text-gray-900 whitespace-nowrap">{patient.inacbg}</td>
              <td className="px-4 py-4 text-sm text-gray-600 whitespace-nowrap">{patient.birth_date}</td>
              <td className="px-4 py-4 text-sm text-gray-600 whitespace-nowrap">{patient.birth_weight}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
