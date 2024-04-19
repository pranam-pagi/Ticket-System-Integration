<template>
  <div class="container">
    <div class="row">
      <div class="col-sm">
        <h1 class="text-center">Add Ticket</h1>
        <form @submit.prevent="addCard">
          <div class="form-group">
            <label>Title </label>
            <i
              class="bi bi-patch-question-fill"
              data-toggle="tooltip"
              data-placement="top"
              title="As you type the title, similar queries will appear on the right. Please read them before creating a new ticket."
            ></i>
            <input
              type="text"
              v-model="title"
              class="form-control"
              placeholder="Enter title"
              autocomplete="off"
              required
            />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea
              v-model="description"
              class="form-control"
              placeholder="Enter description"
              autocomplete="off"
              required
              rows="10"
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
      <div class="vr"></div>
      <div class="col-sm">
        <div class="container overflow-auto">
          <p v-if="results">
            Please look at the following similar tickets before posting a new
            query
          </p>
          <div
            class="search-result"
            v-for="(result, index) in results"
            :key="index"
          >
            <h3>
              <RouterLink
                :to="{
                  name: 'response',
                  params: { ticketId: result.ticket_id },
                }"
              >
                <div v-html="result._highlightResult.title.value"></div>
              </RouterLink>
            </h3>
            <div v-html="result._highlightResult.description.value"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AddTicketComponent",
  data() {
    return {
      title: "",
      description: "",
      results: null,
      ticket: null,
    };
  },
  watch: {
    title: async function (val) {
      let url =
        "https://ONID3NGIHD-dsn.algolia.net/1/indexes/sociogrammers_app/query";
      // eslint-disable-next-line
      let config = {
        headers: {
          "X-Algolia-Application-Id": "ONID3NGIHD",
          "X-Algolia-API-Key": "75a0ed6374006251bc6ec7f3c6c267f2",
        },
      };
      // eslint-disable-next-line
      let data = {
        query: val,
      };
      var instance = axios.create();
      delete instance.defaults.headers.common["secret_authtoken"];
      const response = await instance.post(url, data, config);
      this.results = response.data.hits;
    },
  },
  methods: {
    async addCard() {
      var data = {
        title: this.title,
        description: this.description,
        number_of_upvotes: 0,
        is_read: false,
        is_open: true,
        is_offensive: false,
        is_FAQ: false,
      };
      data = JSON.stringify(data);
      console.log(data);
      await axios
        .post("/api/ticket", data, {
          headers: {
            // "secret_authtoken": localStorage.getItem("token"),
            "Content-Type": "application/json",
          },
        })
        .then((res) => {
          console.log(res);
          if (res.status == 200) {
            axios
              .get("/api/ticket")
              .then((resp) => {
                if (resp.status == 200) {
                  this.ticket = resp.data.data[resp.data.data.length - 1];
                  console.log(this.ticket.ticket_id);

                  axios
                    .post(
                      "/api/v1/discourse/create/post",
                      {
                        title: this.title,
                        message_body: this.description,
                        category: "general",
                        ticket_id: this.ticket.ticket_id,
                      },
                      {
                        headers: {
                          "Content-Type": "application/json",
                        },
                      }
                    )
                    .then((res) => {
                      if (res.status == 200) {
                        console.log(res);
                      }
                    })
                    .catch((err) => {
                      console.log(err);
                    });
                }
              })
              .catch((error) => {
                console.log(error);
              });
            alert("Ticket Added Successfully");
            this.$router.push("/dashboard");
          } else {
            alert(res.data.message);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
.container {
  font-family: "Muli", sans-serif;
  /* display: flex;
     */
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 75vh;
  overflow: hidden;
  margin-top: 75px;
}

label {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 5px;
}

h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}
.topic-container {
  margin: 33px 63px;
}

.ticket-title {
  font-weight: bold;
  font-size: 25px;
}
</style>
