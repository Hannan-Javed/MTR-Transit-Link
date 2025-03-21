package com.example.mtrtransitlink

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.util.Arrays

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Load JSON files from assets and convert them to a list of StationData
        val stationDataList = loadStationData()

        // Set up RecyclerView
        val recyclerView: RecyclerView = findViewById(R.id.recyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = StationAdapter(stationDataList)
    }

    // Load all JSON files from the assets folder
    private fun loadStationData(): List<StationData> {
        val stationDataList = mutableListOf<StationData>()

        // List all files in the assets folder
        val assetManager = assets
        val files = assetManager.list("closest_compartments") ?: return emptyList()

        for (fileName in files) {
            if (fileName.endsWith(".json")) {
                val jsonString = assetManager.open("closest_compartments/$fileName").bufferedReader().use(BufferedReader::readText)
                val jsonObject = JSONObject(jsonString)
                val stationData = parseJson(fileName.substring(0, fileName.length - 5), jsonObject)
                stationDataList.add(stationData)
            }
        }

        return stationDataList
    }

    // Parse JSON into a StationData object
    private fun parseJson(fileName: String, jsonObject: JSONObject): StationData {
        val stationRoutes = mutableListOf<StationRoute>()

        for (routeName in jsonObject.keys()) {
            val exitsObject = jsonObject.getJSONObject(routeName)
            val exits = mutableListOf<ExitData>()

            for (exitName in exitsObject.keys()) {
                val direction = exitsObject.getString(exitName)
                exits.add(ExitData(exitName, direction))
            }
            Log.e("exits", routeName)
            stationRoutes.add(StationRoute(routeName, exits))
        }

        return StationData(fileName, stationRoutes)
    }
}

data class StationData(
    val name: String,
    val routes: List<StationRoute>
)

data class StationRoute(
    val name: String,
    val exits: List<ExitData>
)

data class ExitData(
    val name: String,
    val direction: String
)