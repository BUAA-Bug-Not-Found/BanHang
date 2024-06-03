const timeSlots = [
  "8:00-8:45", "8:50-9:35", "9:50-10:35", "10:40-11:25",
  "11:30-12:45", "14:00-14:45", "14:50-15:35", "15:50-16:35",
  "16:40-17:25", "17:30-18:15", "19:00-19:45", "19:50-20:35",
  "20:50-21:35", "21:40-22:25", "23:00-23:00"
];

function getCurrentClassSlot() {
  const now = new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const time = hours * 60 + minutes;

  const slotTimes = [
    [480, 525], [530, 575], [590, 635], [640, 685],
    [690, 765], [840, 885], [890, 935], [950, 995],
    [1000, 1045], [1050, 1095], [1140, 1185], [1190, 1235],
    [1250, 1295], [1300, 1345]
  ];

  for (let i = 0; i < slotTimes.length; i++) {
    if (time >= slotTimes[i][0] && time <= slotTimes[i][1]) {
      return i + 1;
    }
  }
  return -1;
}


function convertToMinutes(time) {
  const [hours, minutes] = time.split(':').map(Number);
  return hours * 60 + minutes;
}

export function processVacantClassrooms(data) {
  const currentClassSlot = getCurrentClassSlot();
  for (const campus in data) {
    data[campus].buildings.forEach(building => {
      building.vacantClassroomInfo = building.vacantClassroomInfo
        .filter(classroom => classroom.vacant_time.includes(currentClassSlot))
        .map(classroom => {
          let maxVacantTime = currentClassSlot;
          while (classroom.vacant_time.includes(maxVacantTime + 1)) {
            maxVacantTime++;
          }
          classroom.vacent_time_end = timeSlots[maxVacantTime].split('-')[0];
          return classroom;
        })
        .sort((a, b) => {
          return convertToMinutes(b.vacent_time_end) - convertToMinutes(a.vacent_time_end)
        });
    });
  }
  return data;
}

