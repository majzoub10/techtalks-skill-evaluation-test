document.addEventListener("DOMContentLoaded", function () {

    fetch("/api/admin/dashboard")
        .then(response => response.json())
        .then(data => {

            console.log(data); 

            document.getElementById("totalUsers").innerText = data.total_users;
            document.getElementById("totalSkills").innerText = data.total_skills;
            document.getElementById("highestScore").innerText = data.highest_score + "%";
            document.getElementById("highestSkillName").innerText = data.highest_skill_name;

            const ctx = document.getElementById("avgScoreChart");

            if (!ctx) {
                console.error("Canvas not found");
                return;
            }

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.skill_names,
                    datasets: [{
                        label: "Average Skill Score",
                        data: data.skill_avg_scores,
                        backgroundColor: "#3b82f6"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

        })
        .catch(error => console.error(error));

});
