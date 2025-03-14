package com.example.mtrtransitlink

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView

class StationAdapter(private val stationDataList: List<StationData>) :
    RecyclerView.Adapter<StationAdapter.StationViewHolder>() {

    private val expandedPositions = mutableSetOf<Int>() // Tracks expanded items

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): StationViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_station, parent, false)
        return StationViewHolder(view)
    }

    override fun onBindViewHolder(holder: StationViewHolder, position: Int) {
        val stationData = stationDataList[position]
        holder.stationName.text = stationData.name

        // Toggle expansion
        val isExpanded = expandedPositions.contains(position)
        holder.childRecyclerView.visibility = if (isExpanded) View.VISIBLE else View.GONE
        holder.arrow.rotation = if (isExpanded) 180f else 0f

        // Set up child RecyclerView
        holder.childRecyclerView.layoutManager = LinearLayoutManager(holder.itemView.context)
        holder.childRecyclerView.adapter = RouteAdapter(stationData.routes)

        // Handle click on the row
        holder.itemView.setOnClickListener {
            if (isExpanded) {
                expandedPositions.remove(position)
            } else {
                expandedPositions.add(position)
            }
            notifyItemChanged(position)
        }
    }

    override fun getItemCount(): Int = stationDataList.size

    class StationViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val stationName: TextView = itemView.findViewById(R.id.stationName)
        val arrow: ImageView = itemView.findViewById(R.id.arrow)
        val childRecyclerView: RecyclerView = itemView.findViewById(R.id.childRecyclerView)
    }
}