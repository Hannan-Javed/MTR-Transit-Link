package com.example.mtrtransitlink

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class RouteAdapter(private val routes: List<StationRoute>) :
    RecyclerView.Adapter<RouteAdapter.RouteViewHolder>() {

    private val expandedPositions = mutableSetOf<Int>() // Tracks expanded items

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RouteViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_route, parent, false)
        return RouteViewHolder(view)
    }

    override fun onBindViewHolder(holder: RouteViewHolder, position: Int) {
        val route = routes[position]
        holder.routeName.text = route.name

        // Toggle expansion
        val isExpanded = expandedPositions.contains(position)
        holder.exitsContainer.visibility = if (isExpanded) View.VISIBLE else View.GONE
        holder.arrow.rotation = if (isExpanded) 180f else 0f

        // Populate exits
        holder.exitsContainer.removeAllViews()
        for (exit in route.exits) {
            val exitView = LayoutInflater.from(holder.itemView.context)
                .inflate(R.layout.item_exit, holder.exitsContainer, false)
            val exitText: TextView = exitView.findViewById(R.id.exitText)
            exitText.text = "Exit ${exit.name}: Please go to ${exit.direction} of the train."
            holder.exitsContainer.addView(exitView)
        }

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

    override fun getItemCount(): Int = routes.size

    class RouteViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val routeName: TextView = itemView.findViewById(R.id.routeName)
        val arrow: ImageView = itemView.findViewById(R.id.arrow)
        val exitsContainer: ViewGroup = itemView.findViewById(R.id.exitsContainer)
    }
}